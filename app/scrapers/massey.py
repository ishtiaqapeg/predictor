from datetime import date
from typing import List, Optional
import re
from selectolax.parser import HTMLParser
from .base import Scraper, RawGame

class MasseyScraper(Scraper):
    source = "massey"
    
    async def fetch_today(self) -> List[RawGame]:
        """Парсинг MasseyRatings"""
        games = []
        
        try:
            # Пробуем разные URL для Massey Ratings
            urls = [
                "https://masseyratings.com/cb/ncaa-d1/games",
                "https://masseyratings.com/cb/",
                "https://masseyratings.com/",
                "https://masseyratings.com/cb/ncaa-d1/",
                "https://masseyratings.com/cb/ncaa-d1/schedule"
            ]
            
            for url in urls:
                try:
                    response = await self.session.get(url)
                    response.raise_for_status()
                    
                    await self._delay()
                    
                    html = HTMLParser(response.text)
                    
                    # Ищем таблицы с играми
                    tables = html.css("table")
                    if tables:
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
                                            print(f"MasseyRatings: ошибка парсинга строки: {e}")
                                            continue
                                if games:  # Если нашли игры, выходим
                                    break
                        if games:
                            break
                            
                except Exception as e:
                    print(f"MasseyRatings: ошибка с URL {url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"MasseyRatings scraper error: {e}")
            # Не поднимаем исключение, просто возвращаем пустой список
            return []
        
        return games
    
    def _parse_game_row(self, cells) -> Optional[RawGame]:
        """Парсинг строки игры из MasseyRatings"""
        try:
            # Ищем команды и время в разных колонках
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
            print(f"MasseyRatings: ошибка парсинга строки: {e}")
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
