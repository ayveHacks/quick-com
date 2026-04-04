import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.mongodb import get_database
from app.services.monitoring_service import run_monitoring_cycle

logger = logging.getLogger(__name__)


def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")
    return scheduler


async def run_scheduled_monitoring() -> None:
    db = get_database()
    summary = await run_monitoring_cycle(db)
    logger.info("Scheduled monitoring run: %s", summary)

