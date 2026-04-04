import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.indexes import ensure_indexes
from app.db.mongodb import close_mongo_connection, connect_to_mongo, get_database
from app.tasks.scheduler import run_scheduled_monitoring, start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-Powered Parametric Insurance for Quick Commerce Delivery Partners",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "status": "ok",
        "docs": "/docs",
    }


@app.on_event("startup")
async def on_startup() -> None:
    await connect_to_mongo()
    db = get_database()
    await ensure_indexes(db)

    if settings.scheduler_enabled:
        scheduler = start_scheduler()
        scheduler.add_job(
            run_scheduled_monitoring,
            trigger="interval",
            minutes=settings.scheduler_interval_minutes,
            id="disruption-monitoring-job",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
        )
        scheduler.start()
        app.state.scheduler = scheduler
        logger.info("Scheduler started with interval %s minutes", settings.scheduler_interval_minutes)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    scheduler = getattr(app.state, "scheduler", None)
    if scheduler:
        scheduler.shutdown(wait=False)
    await close_mongo_connection()

