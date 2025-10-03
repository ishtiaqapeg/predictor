from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from .tasks import ingest_today

def start_scheduler():
    """Запуск планировщика задач"""
    scheduler = AsyncIOScheduler(timezone=timezone("America/New_York"))
    
    # Добавляем задачу на 12:00 ET каждый день
    scheduler.add_job(
        ingest_today,
        "cron",
        hour=12,
        minute=0,
        id="daily_ingest",
        replace_existing=True
    )
    
    scheduler.start()
    print("Scheduler started - daily ingest at 12:00 ET")
