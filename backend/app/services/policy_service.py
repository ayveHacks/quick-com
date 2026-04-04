from datetime import timedelta
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.premium_engine import compute_policy_pricing
from app.services.risk_engine import calculate_risk_profile
from app.utils.ids import serialize_document, to_object_id
from app.utils.time import utc_now


async def get_active_policy(db: AsyncIOMotorDatabase, worker_id: str | ObjectId) -> dict[str, Any] | None:
    policy = await db.policies.find_one(
        {
            "worker_id": str(worker_id),
            "status": "active",
            "end_date": {"$gte": utc_now()},
            "remaining_coverage": {"$gt": 0},
        }
    )
    return serialize_document(policy)


async def create_policy_for_worker(db: AsyncIOMotorDatabase, worker: dict[str, Any]) -> dict[str, Any]:
    await db.policies.update_many(
        {"worker_id": str(worker["_id"]), "status": "active"},
        {"$set": {"status": "expired", "updated_at": utc_now()}},
    )

    risk_profile = calculate_risk_profile(worker)
    pricing = compute_policy_pricing(worker, risk_profile)

    now = utc_now()
    policy_doc = {
        "worker_id": str(worker["_id"]),
        "status": "active",
        "start_date": now,
        "end_date": now + timedelta(days=7),
        "duration_days": 7,
        "max_claims_per_week": 8,
        "claims_used": 0,
        "remaining_coverage": pricing["coverage_amount"],
        "coverage_amount": pricing["coverage_amount"],
        "premium_amount": pricing["premium_amount"],
        "risk_score": risk_profile["risk_score"],
        "exposure_score": risk_profile["exposure_score"],
        "reliability_score": risk_profile["reliability_score"],
        "coverage_factor": pricing["coverage_factor"],
        "base_rate": pricing["base_rate"],
        "pricing_tier": pricing["pricing_tier"],
        "disruption_probabilities": risk_profile["probabilities"],
        "reliability_breakdown": risk_profile["reliability_breakdown"],
        "created_at": now,
        "updated_at": now,
    }

    result = await db.policies.insert_one(policy_doc)
    policy_doc["_id"] = result.inserted_id

    await db.workers.update_one(
        {"_id": worker["_id"]},
        {
            "$set": {
                "current_risk_score": risk_profile["risk_score"],
                "current_exposure_score": risk_profile["exposure_score"],
                "current_reliability_score": risk_profile["reliability_score"],
                "updated_at": now,
            }
        },
    )

    return serialize_document(policy_doc)


async def renew_expired_policies(db: AsyncIOMotorDatabase) -> int:
    now = utc_now()
    expired_policies = db.policies.find({"status": "active", "end_date": {"$lt": now}})

    renewed_count = 0
    async for policy in expired_policies:
        await db.policies.update_one(
            {"_id": policy["_id"]},
            {"$set": {"status": "expired", "updated_at": now}},
        )

        worker = await db.workers.find_one({"_id": to_object_id(policy["worker_id"])})
        if worker:
            await create_policy_for_worker(db, worker)
            renewed_count += 1

    return renewed_count

