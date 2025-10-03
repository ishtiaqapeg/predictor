from dataclasses import dataclass
from datetime import date
from typing import List, Optional
import asyncio
import httpx
from app.settings import settings

@dataclass
class RawGame:
    date: date
    tipoff_et: Optional[str]
    home: str
    away: str
    neutral: bool
    metrics: dict  # что-то вроде {"spread": ..., "total": ..., "winProbHome": ...}

class Scraper:
    source: str
    
    def __init__(self):
        self.session = httpx.AsyncClient(
            headers={"User-Agent": settings.USER_AGENT},
            timeout=30.0,
            follow_redirects=True
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.aclose()
    
    async def _delay(self):
        """Задержка между запросами к одному домену"""
        await asyncio.sleep(settings.HOST_DELAY_MS / 1000.0)
    
    async def fetch_today(self) -> List[RawGame]:
        raise NotImplementedError
    
    def _parse_float(self, text: str) -> Optional[float]:
        """Безопасное извлечение float из текста"""
        if not text:
            return None
        try:
            # Убираем лишние символы и пробелы
            cleaned = text.strip().replace(',', '').replace('$', '').replace('%', '')
            return float(cleaned)
        except (ValueError, TypeError):
            return None
    
    def _parse_int(self, text: str) -> Optional[int]:
        """Безопасное извлечение int из текста"""
        if not text:
            return None
        try:
            cleaned = text.strip().replace(',', '').replace('$', '').replace('%', '')
            return int(float(cleaned))
        except (ValueError, TypeError):
            return None
