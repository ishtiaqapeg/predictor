from datetime import date
from typing import List, Optional
import re
from selectolax.parser import HTMLParser
from .base import Scraper, RawGame

class HaslaScraper(Scraper):
    source = "hasla"
    
    async def fetch_today(self) -> List[RawGame]:
        """Парсинг Haslametrics (последняя таблица игр дня)"""
        games = []
        
        try:
            url = "https://haslametrics.com/"
            response = await self.session.get(url)
            response.raise_for_status()
            
            await self._delay()
            
            html = HTMLParser(response.text)
            
            # Ищем последнюю таблицу с играми дня
            tables = html.css("table")
            if not tables:
                raise RuntimeError("Haslametrics: не найдены таблицы с играми")
            
            # Берем последнюю таблицу (предполагаем что это сегодняшние игры)
            table = tables[-1]
            
            rows = table.css("tr")
            for row in rows[1:]:  # Пропускаем заголовок
                cells = row.css("td")
                if len(cells) < 6:
                    continue
                
                try:
                    game_data = self._parse_game_row(cells)
                    if game_data:
                        games.append(game_data)
                except Exception as e:
                    print(f"Haslametrics: ошибка парсинга строки: {e}")
                    continue
                    
        except Exception as e:
            print(f"Haslametrics scraper error: {e}")
            raise RuntimeError(f"Haslametrics: {str(e)}")
        
        return games
    
    def _parse_game_row(self, cells) -> Optional[RawGame]:
        """Парсинг строки игры из Haslametrics"""
        try:
            # Структура Haslametrics таблицы
            time_text = cells[0].text(strip=True)
            away_team = cells[1].text(strip=True)
            home_team = cells[2].text(strip=True)
            
            if not away_team or not home_team:
                return None
            
            # Парсим время
            tipoff_et = self._parse_time(time_text)
            
            # Парсим метрики
            spread = self._parse_float(cells[3].text(strip=True)) if len(cells) > 3 else None
            total = self._parse_float(cells[4].text(strip=True)) if len(cells) > 4 else None
            win_prob = self._parse_float(cells[5].text(strip=True)) if len(cells) > 5 else None
            
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
            print(f"Haslametrics: ошибка парсинга строки: {e}")
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
