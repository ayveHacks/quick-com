from datetime import timedelta

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_db
from app.models.disruption import DisruptionEventCreate
from app.services.monitoring_service import create_manual_disruption, run_monitoring_cycle
from app.services.seed_service import seed_demo_data
from app.utils.time import utc_now

router = APIRouter()


@router.post("/seed")
async def seed_data(db: AsyncIOMotorDatabase = Depends(get_db)):
    summary = await seed_demo_data(db)
    return {
        "success": True,
        "message": "Demo data seeded",
        "summary": summary,
    }


@router.post("/run-monitoring")
async def run_monitoring_manual(db: AsyncIOMotorDatabase = Depends(get_db)):
    summary = await run_monitoring_cycle(db)
    return {
        "success": True,
        "message": "Manual monitoring cycle completed",
        "summary": summary,
    }


@router.post("/trigger-disruption")
async def trigger_disruption(event: DisruptionEventCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    now = utc_now()

    disruption_doc = {
        "type": event.type,
        "severity": max(0.1, min(event.severity, 1.0)),
        "city": event.city,
        "affected_zones": event.affected_zones,
        "start_time": now,
        "end_time": now + timedelta(hours=max(0.5, event.duration_hours)),
        "source": "manual-simulation",
        "trigger_metrics": {
            "manual": True,
            "severity": event.severity,
        },
        "created_at": now,
    }

    created = await create_manual_disruption(db, disruption_doc)

    return {
        "success": True,
        "message": "Disruption triggered and claims auto-processed",
        "event": created,
    }

