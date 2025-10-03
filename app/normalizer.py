import csv
import io
import re
import httpx
from unidecode import unidecode
from typing import Dict

def normalize(s: str) -> str:
    """Нормализация названия команды для сопоставления"""
    if not s:
        return ""
    
    s = unidecode(s).lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("&", "and")
    s = re.sub(r"\bst\.?\b", "state", s)
    s = re.sub(r"\b(u|univ)\.?\b", "university", s)
    return s

async def load_alias_map(csv_url: str) -> Dict[str, str]:
    """Загрузка словаря алиасов команд из Google Sheet или локального файла"""
    if csv_url.startswith("file://"):
        # Локальный файл
        file_path = csv_url.replace("file://", "")
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
    else:
        # HTTP URL
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(csv_url)
            response.raise_for_status()
        data = response.content.decode("utf-8")
    
    alias_map = {}
    
    for row in csv.DictReader(io.StringIO(data)):
        # Ожидаем колонки: alias, canonical (переименуйте под вашу таблицу)
        if "alias" in row and "canonical" in row:
            alias = normalize(row["alias"])
            canonical = row["canonical"].strip()
            if alias and canonical:
                alias_map[alias] = canonical
    
    return alias_map

def canon_name(raw: str, alias_map: Dict[str, str]) -> str | None:
    """Получение канонического названия команды по алиасу"""
    if not raw:
        return None
    
    key = normalize(raw)
    return alias_map.get(key)
