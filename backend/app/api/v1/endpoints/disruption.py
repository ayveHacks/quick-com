from datetime import timedelta

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_db
from app.utils.ids import serialize_document
from app.utils.time import utc_now

router = APIRouter()


@router.get("/live")
async def live_disruptions(
    zone: str | None = Query(default=None),
    city: str | None = Query(default=None),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    query: dict = {"end_time": {"$gte": utc_now()}}
    if zone:
        query["affected_zones"] = zone
    if city:
        query["city"] = city

    events = await db.disruptions.find(query).sort("severity", -1).to_list(length=100)
    return {"success": True, "items": [serialize_document(item) for item in events]}


@router.get("/history")
async def disruption_history(
    days: int = Query(default=7, ge=1, le=30),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    since = utc_now() - timedelta(days=days)
    events = (
        await db.disruptions.find({"start_time": {"$gte": since}})
        .sort("start_time", -1)
        .to_list(length=500)
    )
    return {"success": True, "items": [serialize_document(item) for item in events]}

