from datetime import date
from typing import List, Dict
from .models import PredictorRow, SourceMetrics
from statistics import mean

def game_key(d: str, home: str, away: str, neutral: bool) -> str:
    """Создание уникального ключа для игры"""
    return f"{d}|{home}|{away}|{int(neutral)}"

def attach(rows: Dict[str, PredictorRow], dISO: str, tipoff: str, neutral: bool, 
           home: str, away: str, source: str, metrics: dict):
    """Прикрепление метрик источника к игре"""
    key = game_key(dISO, home, away, neutral)
    pr = rows.get(key)
    
    if not pr:
        pr = PredictorRow(
            dateISO=dISO,
            tipoffET=tipoff,
            neutral=neutral,
            homeTeam=home,
            awayTeam=away
        )
        rows[key] = pr
    
    # Устанавливаем метрики для источника
    setattr(pr, source, SourceMetrics(**metrics))

def finalize(rows: Dict[str, PredictorRow]) -> List[PredictorRow]:
    """Финализация данных - вычисление средних значений"""
    out = []
    
    for pr in rows.values():
        # Собираем все доступные значения для вычисления средних
        spreads = []
        totals = []
        win_probs = []
        
        for source in ["kenpom", "bart", "massey", "hasla"]:
            metrics = getattr(pr, source)
            if metrics:
                if metrics.spread is not None:
                    spreads.append(metrics.spread)
                if metrics.total is not None:
                    totals.append(metrics.total)
                if metrics.winProbHome is not None:
                    win_probs.append(metrics.winProbHome)
        
        # Вычисляем средние значения
        pr.avgSpread = mean(spreads) if spreads else None
        pr.avgTotal = mean(totals) if totals else None
        pr.avgWinProbHome = mean(win_probs) if win_probs else None
        
        out.append(pr)
    
    return out
