from random import uniform

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_db
from app.core.security import create_access_token
from app.models.auth import OTPRequest
from app.models.worker import WorkerLoginRequest, WorkerRegistrationRequest
from app.services.otp_service import create_otp_session, verify_otp_session
from app.services.policy_service import create_policy_for_worker
from app.utils.ids import serialize_document
from app.utils.time import utc_now

router = APIRouter()


@router.post("/request-otp")
async def request_otp(payload: OTPRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    otp = await create_otp_session(db, payload.phone)
    return {
        "success": True,
        "message": "OTP generated (simulation mode)",
        "phone": payload.phone,
        "otp": otp,
        "expires_in_minutes": 5,
    }


@router.post("/register")
async def register_worker(payload: WorkerRegistrationRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    otp_ok = await verify_otp_session(db, payload.phone, payload.otp)
    if not otp_ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    existing = await db.workers.find_one({"phone": payload.phone})
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Worker already registered")

    existing_worker_id = await db.workers.find_one({"worker_id": payload.worker_id})
    if existing_worker_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Worker ID already exists")

    now = utc_now()
    completed_orders = int(payload.avg_orders_per_hour * payload.working_hours_per_day * 6)

    worker_doc = {
        "name": payload.name,
        "age": payload.age,
        "phone": payload.phone,
        "delivery_platform": payload.delivery_platform,
        "worker_id": payload.worker_id,
        "city": payload.city,
        "state": payload.state,
        "zone": payload.zone,
        "weekly_income": payload.weekly_income,
        "experience_months": payload.experience_months,
        "avg_orders_per_hour": payload.avg_orders_per_hour,
        "working_hours_per_day": payload.working_hours_per_day,
        "gps_permission": payload.gps_permission,
        "upi_id": payload.upi_id,
        "completed_orders": completed_orders,
        "assigned_orders": max(completed_orders + 15, 1),
        "weekly_working_hours": round(payload.working_hours_per_day * 6, 2),
        "fraud_flags": round(uniform(0.01, 0.07), 3),
        "created_at": now,
        "updated_at": now,
    }

    result = await db.workers.insert_one(worker_doc)
    worker_doc["_id"] = result.inserted_id

    policy = await create_policy_for_worker(db, worker_doc)

    token = create_access_token(subject=str(result.inserted_id), extra={"phone": payload.phone})

    return {
        "success": True,
        "message": "Worker registered successfully",
        "access_token": token,
        "token_type": "bearer",
        "worker": serialize_document(worker_doc),
        "policy": policy,
    }


@router.post("/login")
async def login_worker(payload: WorkerLoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    otp_ok = await verify_otp_session(db, payload.phone, payload.otp)
    if not otp_ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    worker = await db.workers.find_one({"phone": payload.phone})
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not registered")

    policy = await db.policies.find_one(
        {
            "worker_id": str(worker["_id"]),
            "status": "active",
            "end_date": {"$gte": utc_now()},
        }
    )
    if not policy:
        policy = await create_policy_for_worker(db, worker)
    else:
        policy = serialize_document(policy)

    token = create_access_token(subject=str(worker["_id"]), extra={"phone": payload.phone})

    return {
        "success": True,
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "worker": serialize_document(worker),
        "policy": policy,
    }

