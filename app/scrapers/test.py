from datetime import date
from typing import List
from .base import Scraper, RawGame

class TestScraper(Scraper):
    source = "test"
    
    async def fetch_today(self) -> List[RawGame]:
        """Тестовый скрейпер с фиктивными данными"""
        # Создаем несколько тестовых игр
        games = [
            RawGame(
                date=date.today(),
                tipoff_et="19:00",
                home="Duke",
                away="North Carolina",
                neutral=False,
                metrics={
                    "spread": -5.5,
                    "total": 145.5,
                    "winProbHome": 0.65,
                    "projHome": 75.5,
                    "projAway": 70.0,
                    "moneylineHome": -200,
                    "moneylineAway": 170
                }
            ),
            RawGame(
                date=date.today(),
                tipoff_et="21:00",
                home="Kentucky",
                away="Tennessee",
                neutral=False,
                metrics={
                    "spread": -3.0,
                    "total": 142.0,
                    "winProbHome": 0.58,
                    "projHome": 72.5,
                    "projAway": 69.5,
                    "moneylineHome": -150,
                    "moneylineAway": 130
                }
            ),
            RawGame(
                date=date.today(),
                tipoff_et="20:30",
                home="Kansas",
                away="Baylor",
                neutral=False,
                metrics={
                    "spread": -2.5,
                    "total": 138.5,
                    "winProbHome": 0.55,
                    "projHome": 70.5,
                    "projAway": 68.0,
                    "moneylineHome": -140,
                    "moneylineAway": 120
                }
            )
        ]
        
        return games
