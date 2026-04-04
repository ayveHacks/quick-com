from datetime import timedelta

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_worker, get_db
from app.services.policy_service import create_policy_for_worker
from app.utils.ids import serialize_document
from app.utils.time import utc_now

router = APIRouter()


@router.get("/me")
async def get_profile(
    current_worker: dict = Depends(get_current_worker),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    policy = await db.policies.find_one(
        {
            "worker_id": str(current_worker["_id"]),
            "status": "active",
            "end_date": {"$gte": utc_now()},
        }
    )

    return {
        "success": True,
        "worker": serialize_document(current_worker),
        "policy": serialize_document(policy),
    }


@router.get("/me/dashboard")
async def get_worker_dashboard(
    current_worker: dict = Depends(get_current_worker),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    policy = await db.policies.find_one(
        {
            "worker_id": str(current_worker["_id"]),
            "status": "active",
            "end_date": {"$gte": utc_now()},
        }
    )

    if not policy:
        policy = await create_policy_for_worker(db, current_worker)
    else:
        policy = serialize_document(policy)

    disruptions = (
        await db.disruptions.find(
            {
                "affected_zones": current_worker["zone"],
                "end_time": {"$gte": utc_now() - timedelta(hours=3)},
            }
        )
        .sort("start_time", -1)
        .to_list(length=20)
    )

    claims = (
        await db.claims.find({"worker_id": str(current_worker["_id"])})
        .sort("created_at", -1)
        .to_list(length=30)
    )

    notifications = (
        await db.payout_notifications.find({"worker_id": str(current_worker["_id"])})
        .sort("created_at", -1)
        .to_list(length=20)
    )

    return {
        "success": True,
        "worker": serialize_document(current_worker),
        "policy": policy,
        "live_disruptions": [serialize_document(item) for item in disruptions],
        "claims": [serialize_document(item) for item in claims],
        "payout_notifications": [serialize_document(item) for item in notifications],
    }


@router.get("/me/claims")
async def get_worker_claims(
    current_worker: dict = Depends(get_current_worker),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    claims = (
        await db.claims.find({"worker_id": str(current_worker["_id"])})
        .sort("created_at", -1)
        .to_list(length=100)
    )
    return {
        "success": True,
        "items": [serialize_document(item) for item in claims],
    }


@router.get("/me/disruptions")
async def get_worker_disruptions(
    current_worker: dict = Depends(get_current_worker),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    events = (
        await db.disruptions.find(
            {
                "affected_zones": current_worker["zone"],
                "start_time": {"$gte": utc_now() - timedelta(days=3)},
            }
        )
        .sort("start_time", -1)
        .to_list(length=100)
    )

    return {
        "success": True,
        "items": [serialize_document(item) for item in events],
    }


@router.patch("/me/activity")
async def patch_activity(
    payload: dict,
    current_worker: dict = Depends(get_current_worker),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    updates = {
        "completed_orders": max(int(payload.get("completed_orders", current_worker.get("completed_orders", 0))), 0),
        "assigned_orders": max(int(payload.get("assigned_orders", current_worker.get("assigned_orders", 1))), 1),
        "weekly_working_hours": max(float(payload.get("weekly_working_hours", current_worker.get("weekly_working_hours", 48))), 1),
        "updated_at": utc_now(),
    }

    await db.workers.update_one({"_id": current_worker["_id"]}, {"$set": updates})
    updated = await db.workers.find_one({"_id": current_worker["_id"]})

    policy = await create_policy_for_worker(db, updated)

    return {
        "success": True,
        "message": "Activity updated and policy repriced",
        "worker": serialize_document(updated),
        "policy": policy,
    }

