from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_worker, get_db
from app.services.policy_service import create_policy_for_worker
from app.utils.ids import serialize_document
from app.utils.time import utc_now

router = APIRouter()


@router.get("/me/active")
async def get_my_active_policy(
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
    return {"success": True, "policy": serialize_document(policy)}


@router.post("/me/refresh")
async def refresh_my_policy(
    current_worker: dict = Depends(get_current_worker),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    policy = await create_policy_for_worker(db, current_worker)
    return {
        "success": True,
        "message": "Policy repriced and refreshed",
        "policy": policy,
    }

