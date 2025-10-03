#!/usr/bin/env python3
"""
Скрипт для тестирования скрейперов
"""
import asyncio
import sys
import os

# Добавляем путь к приложению
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers import (
    KenPomScraper,
    BartScraper, 
    MasseyScraper,
    HaslaScraper,
    TeamRankingsScraper
)

async def test_scraper(scraper_class, name):
    """Тестирование одного скрейпера"""
    print(f"\n{'='*50}")
    print(f"Testing {name} scraper...")
    print(f"{'='*50}")
    
    try:
        async with scraper_class() as scraper:
            games = await scraper.fetch_today()
            print(f"✅ {name}: Found {len(games)} games")
            
            # Показываем первые несколько игр
            for i, game in enumerate(games[:3]):
                print(f"  Game {i+1}: {game.away} @ {game.home}")
                print(f"    Time: {game.tipoff_et}")
                print(f"    Neutral: {game.neutral}")
                print(f"    Metrics: {game.metrics}")
                print()
                
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)}")

async def main():
    """Основная функция тестирования"""
    print("NCAA D1 Predictor - Scraper Test")
    print("=" * 50)
    
    scrapers = [
        (KenPomScraper, "KenPom"),
        (BartScraper, "BartTorvik"),
        (MasseyScraper, "MasseyRatings"),
        (HaslaScraper, "Haslametrics"),
        (TeamRankingsScraper, "TeamRankings")
    ]
    
    for scraper_class, name in scrapers:
        await test_scraper(scraper_class, name)
        await asyncio.sleep(2)  # Задержка между тестами
    
    print(f"\n{'='*50}")
    print("Scraper testing completed!")
    print(f"{'='*50}")

if __name__ == "__main__":
    asyncio.run(main())
