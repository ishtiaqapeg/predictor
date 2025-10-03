import json
import os
import aioboto3
from .models import Snapshot
from .settings import settings

LOCAL_PATH = "data/today.json"

async def load_snapshot() -> Snapshot | None:
    """Загрузка снимка данных"""
    if settings.DATA_BACKEND == "s3":
        return await _load_from_s3()
    else:
        return await _load_from_local()

async def save_snapshot(snap: Snapshot):
    """Сохранение снимка данных"""
    data = snap.model_dump_json(indent=2)
    
    if settings.DATA_BACKEND == "s3":
        await _save_to_s3(data)
    else:
        await _save_to_local(data)

async def _load_from_s3() -> Snapshot | None:
    """Загрузка из S3"""
    if not all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.S3_BUCKET]):
        print("S3 credentials not configured")
        return None
    
    try:
        session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        
        async with session.client("s3") as s3:
            obj = await s3.get_object(
                Bucket=settings.S3_BUCKET, 
                Key=settings.S3_OBJECT_KEY
            )
            data = await obj["Body"].read()
            return Snapshot.model_validate_json(data)
            
    except Exception as e:
        print(f"Error loading from S3: {e}")
        return None

async def _save_to_s3(data: str):
    """Сохранение в S3"""
    if not all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.S3_BUCKET]):
        print("S3 credentials not configured")
        return
    
    try:
        session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        
        async with session.client("s3") as s3:
            await s3.put_object(
                Bucket=settings.S3_BUCKET,
                Key=settings.S3_OBJECT_KEY,
                Body=data.encode("utf-8"),
                ContentType="application/json"
            )
            
    except Exception as e:
        print(f"Error saving to S3: {e}")
        raise

async def _load_from_local() -> Snapshot | None:
    """Загрузка из локального файла"""
    if not os.path.exists(LOCAL_PATH):
        return None
    
    try:
        with open(LOCAL_PATH, "r", encoding="utf-8") as f:
            data = f.read()
            return Snapshot.model_validate_json(data)
    except Exception as e:
        print(f"Error loading from local file: {e}")
        return None

async def _save_to_local(data: str):
    """Сохранение в локальный файл"""
    os.makedirs("data", exist_ok=True)
    
    try:
        with open(LOCAL_PATH, "w", encoding="utf-8") as f:
            f.write(data)
    except Exception as e:
        print(f"Error saving to local file: {e}")
        raise
