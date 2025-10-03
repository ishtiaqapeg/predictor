#!/usr/bin/env python3
"""
Тестирование реальных скрейперов NCAA D1 Basketball Predictor
"""

import asyncio
import sys
import os
from datetime import date

# Добавляем путь к приложению
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scrapers import (
    KenPomScraper,
    BartScraper, 
    MasseyScraper,
    HaslaScraper,
    TeamRankingsScraper
)

async def test_scraper(scraper_class, name):
    """Тестирование одного скрейпера"""
    print(f"\n🔍 Тестирование {name} скрейпера...")
    print("=" * 50)
    
    try:
        scraper = scraper_class()
        async with scraper:
            games = await scraper.fetch_today()
            
            print(f"✅ {name}: Получено {len(games)} игр")
            
            if games:
                # Показываем первую игру как пример
                game = games[0]
                print(f"📊 Пример игры:")
                print(f"   Команды: {game.away} @ {game.home}")
                print(f"   Время: {game.tipoff_et}")
                print(f"   Нейтральная: {game.neutral}")
                print(f"   Метрики: {game.metrics}")
                
                # Показываем статистику по метрикам
                metrics_count = sum(1 for v in game.metrics.values() if v is not None)
                print(f"   Заполненных метрик: {metrics_count}/7")
            else:
                print("⚠️  Игры не найдены")
                
    except Exception as e:
        print(f"❌ {name}: Ошибка - {str(e)}")
        return False
    
    return True

async def main():
    """Основная функция тестирования"""
    print("🏀 Тестирование реальных скрейперов NCAA D1 Basketball Predictor")
    print("=" * 70)
    
    scrapers = [
        (KenPomScraper, "KenPom"),
        (BartScraper, "BartTorvik"),
        (MasseyScraper, "Massey Ratings"),
        (HaslaScraper, "Haslametrics"),
        (TeamRankingsScraper, "TeamRankings")
    ]
    
    results = []
    
    for scraper_class, name in scrapers:
        success = await test_scraper(scraper_class, name)
        results.append((name, success))
    
    # Итоговый отчет
    print("\n" + "=" * 70)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 70)
    
    working_count = 0
    for name, success in results:
        status = "✅ РАБОТАЕТ" if success else "❌ НЕ РАБОТАЕТ"
        print(f"{name:15} : {status}")
        if success:
            working_count += 1
    
    print(f"\n📈 Результат: {working_count}/{len(results)} скрейперов работают")
    
    if working_count == 0:
        print("\n⚠️  ВНИМАНИЕ: Ни один реальный скрейпер не работает!")
        print("   Это нормально для тестирования - система использует демо-данные")
    elif working_count < len(results):
        print(f"\n⚠️  ВНИМАНИЕ: Только {working_count} из {len(results)} скрейперов работают")
        print("   Система будет использовать доступные источники + демо-данные")
    else:
        print("\n🎉 ОТЛИЧНО: Все скрейперы работают!")
    
    print("\n💡 Рекомендации:")
    print("   - Для продакшена настройте аутентификацию KenPom")
    print("   - Проверьте доступность внешних сайтов")
    print("   - Система автоматически использует fallback на демо-данные")

if __name__ == "__main__":
    asyncio.run(main())
