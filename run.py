#!/usr/bin/env python3
"""
Скрипт запуска NCAA D1 Predictor
"""
import uvicorn
import os
from dotenv import load_dotenv

def main():
    """Запуск приложения"""
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем настройки из переменных окружения
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"Starting NCAA D1 Predictor on {host}:{port}")
    print(f"Reload mode: {reload}")
    
    # Запускаем сервер
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()
