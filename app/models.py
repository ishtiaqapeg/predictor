from pydantic import BaseModel
from typing import Optional, Literal, Dict, List

Source = Literal["kenpom", "bart", "massey", "hasla", "odds"]

class SourceMetrics(BaseModel):
    spread: Optional[float] = None
    total: Optional[float] = None
    winProbHome: Optional[float] = None
    projHome: Optional[float] = None
    projAway: Optional[float] = None
    moneylineHome: Optional[int] = None
    moneylineAway: Optional[int] = None

class PredictorRow(BaseModel):
    dateISO: str                # YYYY-MM-DD
    tipoffET: Optional[str] = None  # HH:MM
    neutral: bool
    awayTeam: str
    homeTeam: str
    kenpom: Optional[SourceMetrics] = None
    bart: Optional[SourceMetrics] = None
    massey: Optional[SourceMetrics] = None
    hasla: Optional[SourceMetrics] = None
    odds: Optional[SourceMetrics] = None
    avgSpread: Optional[float] = None
    avgTotal: Optional[float] = None
    avgWinProbHome: Optional[float] = None

class Snapshot(BaseModel):
    status: Literal["ok", "stale"] = "ok"
    etDate: str                 # YYYY-MM-DD (ET)
    rows: List[PredictorRow] = []
