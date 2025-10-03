from datetime import date, datetime, timedelta
from typing import List
import random
from .base import Scraper, RawGame

class DemoScraper(Scraper):
    source = "demo"
    
    async def fetch_today(self) -> List[RawGame]:
        """Демо скрейпер с реалистичными случайными данными"""
        games = []
        
        # Список реальных команд NCAA D1
        teams = [
            "Duke", "North Carolina", "Kentucky", "Kansas", "Baylor", "Tennessee",
            "Arizona", "UCLA", "Michigan State", "Michigan", "Ohio State", "Purdue",
            "Wisconsin", "Illinois", "Iowa", "Maryland", "Rutgers", "Penn State",
            "Northwestern", "Indiana", "Minnesota", "Nebraska", "Villanova", "UConn",
            "Creighton", "Xavier", "Providence", "Seton Hall", "St. John's", "Butler",
            "DePaul", "Georgetown", "Marquette", "Dayton", "Richmond", "Saint Louis",
            "Davidson", "St. Bonaventure", "Rhode Island", "Massachusetts", "George Mason",
            "La Salle", "Saint Joseph's", "Duquesne", "Fordham", "George Washington",
            "San Diego State", "Nevada", "Utah State", "Boise State", "New Mexico",
            "Colorado State", "Fresno State", "Wyoming", "Air Force", "San Jose State",
            "UNLV", "Houston", "Memphis", "Cincinnati", "Wichita State", "Temple",
            "South Florida", "Tulane", "Tulsa", "East Carolina", "SMU", "UCF",
            "Gonzaga", "Saint Mary's", "BYU", "San Francisco", "Santa Clara", "Pepperdine",
            "Loyola Marymount", "San Diego", "Portland", "Pacific"
        ]
        
        # Генерируем 3-5 игр на сегодня
        num_games = random.randint(3, 5)
        
        for i in range(num_games):
            # Случайные команды
            away_team = random.choice(teams)
            home_team = random.choice([t for t in teams if t != away_team])
            
            # Случайное время (15:00 - 22:00)
            hour = random.randint(15, 22)
            minute = random.choice([0, 15, 30, 45])
            tipoff_et = f"{hour:02d}:{minute:02d}"
            
            # Случайные метрики (реалистичные диапазоны)
            spread = round(random.uniform(-15, 15), 1)
            total = round(random.uniform(120, 180), 1)
            win_prob = round(random.uniform(0.2, 0.8), 3)
            
            # Случайные проекции очков
            total_points = total
            proj_home = round((total_points + spread) / 2, 1)
            proj_away = round((total_points - spread) / 2, 1)
            
            # Случайные moneyline
            if spread > 0:
                ml_home = random.randint(-300, -110)
                ml_away = random.randint(110, 300)
            else:
                ml_home = random.randint(110, 300)
                ml_away = random.randint(-300, -110)
            
            # Случайная нейтральная площадка (10% шанс)
            neutral = random.random() < 0.1
            
            game = RawGame(
                date=date.today(),
                tipoff_et=tipoff_et,
                home=home_team,
                away=away_team,
                neutral=neutral,
                metrics={
                    "spread": spread,
                    "total": total,
                    "winProbHome": win_prob,
                    "projHome": proj_home,
                    "projAway": proj_away,
                    "moneylineHome": ml_home,
                    "moneylineAway": ml_away
                }
            )
            
            games.append(game)
        
        return games

