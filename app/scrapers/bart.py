from datetime import date
from typing import List, Optional
import re
from selectolax.parser import HTMLParser
from .base import Scraper, RawGame

class BartScraper(Scraper):
    source = "bart"
    
    async def fetch_today(self) -> List[RawGame]:
        """Парсинг BartTorvik schedule.php"""
        games = []
        
        try:
            # Пробуем разные URL для BartTorvik
            urls = [
                "https://barttorvik.com/schedule.php",
                "https://barttorvik.com/",
                "https://barttorvik.com/trank.php"
            ]
            
            for url in urls:
                try:
                    # Добавляем больше заголовков для обхода защиты
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    }
                    
                    response = await self.session.get(url, headers=headers)
                    response.raise_for_status()
                    
                    await self._delay()
                    
                    html = HTMLParser(response.text)
                    
                    # Ищем таблицу с играми
                    tables = html.css("table")
                    if tables:
                        # Берем первую таблицу с данными
                        for table in tables:
                            rows = table.css("tr")
                            if len(rows) > 1:  # Есть данные
                                for row in rows[1:]:  # Пропускаем заголовок
                                    cells = row.css("td")
                                    if len(cells) >= 3:  # Минимум 3 колонки
                                        try:
                                            game_data = self._parse_game_row(cells)
                                            if game_data:
                                                games.append(game_data)
                                        except Exception as e:
                                            print(f"BartTorvik: ошибка парсинга строки: {e}")
                                            continue
                                break
                        break
                        
                except Exception as e:
                    print(f"BartTorvik: ошибка с URL {url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"BartTorvik scraper error: {e}")
            # Не поднимаем исключение, просто возвращаем пустой список
            return []
        
        return games
    
    def _parse_game_row(self, cells) -> Optional[RawGame]:
        """Парсинг строки игры из BartTorvik"""
        try:
            # Ищем команды в разных колонках
            away_team = None
            home_team = None
            time_text = None
            
            # Пробуем найти команды в разных позициях
            for i, cell in enumerate(cells):
                text = cell.text(strip=True)
                if not text:
                    continue
                    
                # Если это время
                if re.match(r'\d{1,2}:\d{2}', text) or 'PM' in text or 'AM' in text:
                    time_text = text
                # Если это команда (содержит буквы и не число)
                elif re.search(r'[A-Za-z]', text) and not re.match(r'^\d+\.?\d*$', text):
                    if not away_team:
                        away_team = text
                    elif not home_team:
                        home_team = text
                        break
            
            if not away_team or not home_team:
                return None
            
            # Парсим время
            tipoff_et = self._parse_time(time_text)
            
            # Парсим метрики из оставшихся колонок
            spread = None
            total = None
            win_prob = None
            
            for cell in cells:
                text = cell.text(strip=True)
                if not text:
                    continue
                    
                # Пробуем найти числовые значения
                if re.match(r'^-?\d+\.?\d*$', text):
                    val = self._parse_float(text)
                    if val is not None:
                        # Предполагаем что это spread, total или win_prob
                        if spread is None:
                            spread = val
                        elif total is None:
                            total = val
                        elif win_prob is None:
                            win_prob = val / 100 if val > 1 else val  # Конвертируем проценты
            
            # Определяем нейтральную площадку
            neutral = "neutral" in away_team.lower() or "neutral" in home_team.lower()
            
            return RawGame(
                date=date.today(),
                tipoff_et=tipoff_et,
                home=home_team,
                away=away_team,
                neutral=neutral,
                metrics={
                    "spread": spread,
                    "total": total,
                    "winProbHome": win_prob,
                    "projHome": None,
                    "projAway": None,
                    "moneylineHome": None,
                    "moneylineAway": None
                }
            )
            
        except Exception as e:
            print(f"BartTorvik: ошибка парсинга строки: {e}")
            return None
    
    def _parse_time(self, time_text: str) -> Optional[str]:
        """Парсинг времени в формате ET"""
        if not time_text:
            return None
        
        time_text = time_text.strip()
        
        # Если уже в формате HH:MM, возвращаем как есть
        if re.match(r'^\d{1,2}:\d{2}$', time_text):
            return time_text
        
        # Пытаемся извлечь время из текста
        time_match = re.search(r'(\d{1,2}):(\d{2})', time_text)
        if time_match:
            return f"{time_match.group(1)}:{time_match.group(2)}"
        
        return None
