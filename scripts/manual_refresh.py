#!/usr/bin/env python3
"""
Скрипт для ручного обновления данных
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Добавляем путь к приложению
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tasks import ingest_today

async def main():
    """Ручное обновление данных"""
    print("Starting manual data refresh...")
    
    # Загружаем переменные окружения
    load_dotenv()
    
    try:
        await ingest_today()
        print("✅ Data refresh completed successfully!")
    except Exception as e:
        print(f"❌ Data refresh failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
