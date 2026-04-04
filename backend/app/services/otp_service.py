from datetime import timedelta

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.security import generate_otp
from app.utils.time import utc_now


OTP_TTL_MINUTES = 5


async def create_otp_session(db: AsyncIOMotorDatabase, phone: str) -> str:
    otp = generate_otp()
    now = utc_now()

    await db.otp_sessions.insert_one(
        {
            "phone": phone,
            "otp": otp,
            "created_at": now,
            "expires_at": now + timedelta(minutes=OTP_TTL_MINUTES),
            "used": False,
        }
    )

    return otp


async def verify_otp_session(db: AsyncIOMotorDatabase, phone: str, otp: str) -> bool:
    now = utc_now()
    record = await db.otp_sessions.find_one(
        {
            "phone": phone,
            "otp": otp,
            "used": False,
            "expires_at": {"$gte": now},
        },
        sort=[("created_at", -1)],
    )

    if not record:
        return False

    await db.otp_sessions.update_one({"_id": record["_id"]}, {"$set": {"used": True}})
    return True

