from datetime import timedelta

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.utils.time import utc_now


async def fetch_admin_metrics(db: AsyncIOMotorDatabase) -> dict:
    total_workers = await db.workers.count_documents({})
    active_policies = await db.policies.count_documents({"status": "active", "end_date": {"$gte": utc_now()}})

    premium_pipeline = [
        {"$match": {}},
        {"$group": {"_id": None, "total": {"$sum": "$premium_amount"}}},
    ]
    payout_pipeline = [
        {"$match": {}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}},
    ]
    claims_payout_pipeline = [
        {"$match": {"status": "approved"}},
        {"$group": {"_id": None, "total": {"$sum": "$payout_amount"}}},
    ]

    premium_result = await db.policies.aggregate(premium_pipeline).to_list(1)
    payout_result = await db.payouts.aggregate(payout_pipeline).to_list(1)
    claims_payout_result = await db.claims.aggregate(claims_payout_pipeline).to_list(1)

    total_premium = float(premium_result[0]["total"]) if premium_result else 0.0
    total_payouts_ledger = float(payout_result[0]["total"]) if payout_result else 0.0
    total_payouts_claims = float(claims_payout_result[0]["total"]) if claims_payout_result else 0.0
    total_payouts = max(total_payouts_ledger, total_payouts_claims)

    loss_ratio = (total_payouts / total_premium) if total_premium else 0.0

    fraud_alerts = await db.fraud_logs.count_documents({"created_at": {"$gte": utc_now() - timedelta(days=7)}})
    active_disruptions = await db.disruptions.count_documents({"end_time": {"$gte": utc_now()}})

    return {
        "total_workers": total_workers,
        "active_policies": active_policies,
        "total_premium_collected": round(total_premium, 2),
        "total_payouts": round(total_payouts, 2),
        "loss_ratio": round(loss_ratio, 4),
        "fraud_alerts": fraud_alerts,
        "active_disruptions": active_disruptions,
    }


async def disruption_analytics(db: AsyncIOMotorDatabase) -> list[dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$type",
                "count": {"$sum": 1},
                "avg_severity": {"$avg": "$severity"},
            }
        },
        {"$sort": {"count": -1}},
    ]

    rows = await db.disruptions.aggregate(pipeline).to_list(length=20)
    return [
        {
            "type": row["_id"],
            "count": row["count"],
            "avg_severity": round(float(row["avg_severity"]), 3),
        }
        for row in rows
    ]

