from datetime import datetime
from dateutil import tz
from .settings import settings
from .models import Snapshot
from .storage import save_snapshot
from .normalizer import load_alias_map, canon_name
from .merger import attach, finalize
from .scrapers import (
    KenPomScraper,
    BartScraper,
    MasseyScraper,
    HaslaScraper,
    TeamRankingsScraper
)

async def ingest_today():
    """Основная задача сбора данных за сегодня"""
    print("Starting daily ingest...")
    
    # Рассчитываем «сегодня» в ET
    now_utc = datetime.utcnow().replace(tzinfo=tz.UTC)
    now_et = now_utc.astimezone(tz.gettz("America/New_York"))
    et_date_str = now_et.strftime("%Y-%m-%d")
    
    print(f"Processing games for {et_date_str} (ET)")
    
    # Загружаем словарь команд
    try:
        alias_map = await load_alias_map(settings.TEAMLIST_CSV_URL)
        print(f"Loaded {len(alias_map)} team aliases")
    except Exception as e:
        print(f"Error loading team aliases: {e}")
        # Создаем пустой снимок с ошибкой
        snap = Snapshot(status="stale", etDate=et_date_str, rows=[])
        await save_snapshot(snap)
        return
    
    # Инициализируем только реальные скрейперы
    scrapers = [
        ("kenpom", KenPomScraper()),
        ("bart", BartScraper()),
        ("massey", MasseyScraper()),
        ("hasla", HaslaScraper()),
        ("odds", TeamRankingsScraper()),
    ]
    
    rows_map = {}
    errors = []
    
    # Запускаем все скрейперы
    for name, scraper in scrapers:
        try:
            print(f"Running {name} scraper...")
            async with scraper:
                raw_list = await scraper.fetch_today()
                
                for rg in raw_list:
                    # Проверяем что игра на сегодня
                    if rg.date.strftime("%Y-%m-%d") != et_date_str:
                        continue
                    
                    # Нормализуем названия команд
                    home = canon_name(rg.home, alias_map)
                    away = canon_name(rg.away, alias_map)
                    
                    if not home or not away:
                        print(f"Skipping game {rg.away} @ {rg.home} - teams not found in alias map")
                        continue
                    
                    # Прикрепляем метрики к игре
                    attach(rows_map, et_date_str, rg.tipoff_et, rg.neutral, home, away, name, rg.metrics)
                
                print(f"{name} scraper completed: {len([rg for rg in raw_list if rg.date.strftime('%Y-%m-%d') == et_date_str])} games")
                
        except Exception as e:
            error_msg = f"{name} scraper failed: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            continue

    # Проверяем, получили ли мы данные от реальных скрейперов
    if not rows_map:
        print("No real data available from any scraper")
        print("This is normal during off-season or when sources are unavailable")
    
    # Финализируем данные
    try:
        rows = finalize(rows_map)
        status = "ok" if rows and not errors else "stale"
        
        print(f"Finalized {len(rows)} games, status: {status}")
        if errors:
            print(f"Errors encountered: {errors}")
        
    except Exception as e:
        print(f"Error finalizing data: {e}")
        rows, status = [], "stale"
    
    # Сохраняем снимок
    snap = Snapshot(status=status, etDate=et_date_str, rows=rows)
    await save_snapshot(snap)
    
    print(f"Daily ingest completed. Status: {status}, Games: {len(rows)}")
