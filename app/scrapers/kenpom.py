from datetime import date, datetime
from typing import List, Optional
import re
from selectolax.parser import HTMLParser
from .base import Scraper, RawGame
from app.settings import settings

class KenPomScraper(Scraper):
    source = "kenpom"
    
    async def fetch_today(self) -> List[RawGame]:
        """Парсинг KenPom fanmatch.php"""
        games = []
        
        try:
            # Сначала логинимся если нужно
            if settings.KENPOM_EMAIL and settings.KENPOM_PASSWORD:
                await self._login()
            elif settings.KENPOM_COOKIE:
                self.session.cookies.update({"KPSID": settings.KENPOM_COOKIE})
            
            # Пробуем разные URL для KenPom
            urls = [
                "https://kenpom.com/fanmatch.php",
                "https://kenpom.com/",
                "https://kenpom.com/schedule.php",
                "https://kenpom.com/games.php"
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
                                            print(f"KenPom: ошибка парсинга строки: {e}")
                                            continue
                                if games:  # Если нашли игры, выходим
                                    break
                        if games:
                            break
                            
                except Exception as e:
                    print(f"KenPom: ошибка с URL {url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"KenPom scraper error: {e}")
            raise RuntimeError(f"KenPom: {str(e)}")
        
        return games
    
    async def _login(self):
        """Логин в KenPom"""
        login_url = "https://kenpom.com/login.php"
        
        # Получаем страницу логина
        response = await self.session.get(login_url)
        response.raise_for_status()
        
        # Отправляем данные логина
        login_data = {
            "email": settings.KENPOM_EMAIL,
            "password": settings.KENPOM_PASSWORD
        }
        
        response = await self.session.post(login_url, data=login_data)
        response.raise_for_status()
        
        await self._delay()
    
    def _parse_game_row(self, cells) -> Optional[RawGame]:
        """Парсинг строки игры из KenPom"""
        try:
            # Структура KenPom таблицы может варьироваться
            # Предполагаем формат: время, away, home, spread, total, win_prob, etc.
            
            time_text = cells[0].text(strip=True)
            away_team = cells[1].text(strip=True)
            home_team = cells[2].text(strip=True)
            
            # Проверяем что это игра на сегодня
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
            print(f"KenPom: ошибка парсинга строки: {e}")
            return None
    
    def _parse_time(self, time_text: str) -> Optional[str]:
        """Парсинг времени в формате ET"""
        if not time_text:
            return None
        
        # Убираем лишние символы
        time_text = time_text.strip()
        
        # Если уже в формате HH:MM, возвращаем как есть
        if re.match(r'^\d{1,2}:\d{2}$', time_text):
            return time_text
        
        # Пытаемся извлечь время из текста
        time_match = re.search(r'(\d{1,2}):(\d{2})', time_text)
        if time_match:
            return f"{time_match.group(1)}:{time_match.group(2)}"
        
        return None
