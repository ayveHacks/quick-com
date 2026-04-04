from datetime import timedelta
import hashlib
import math
import random
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.utils.time import utc_now


CITY_COORDS: dict[str, tuple[float, float]] = {
    "Mumbai": (19.076, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Bangalore": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Delhi": (28.6139, 77.209),
    "Hyderabad": (17.385, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Pune": (18.5204, 73.8567),
}


def _bounded(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _rnd(worker_id: str, disruption_id: str) -> random.Random:
    digest = hashlib.sha256(f"{worker_id}:{disruption_id}".encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def _offset_point(lat: float, lon: float, distance_km: float, bearing_deg: float) -> tuple[float, float]:
    # Approximate local shift; good enough for short-distance fraud checks.
    bearing_rad = math.radians(bearing_deg)
    delta_lat = (distance_km / 111.0) * math.cos(bearing_rad)
    lon_scale = max(math.cos(math.radians(lat)), 0.1)
    delta_lon = (distance_km / (111.0 * lon_scale)) * math.sin(bearing_rad)
    return lat + delta_lat, lon + delta_lon


def _simulate_velocity_signal(worker: dict[str, Any], rnd: random.Random) -> dict[str, float | bool]:
    city = worker.get("city", "Mumbai")
    base_lat, base_lon = CITY_COORDS.get(city, CITY_COORDS["Mumbai"])

    prev_lat = base_lat + rnd.uniform(-0.004, 0.004)
    prev_lon = base_lon + rnd.uniform(-0.004, 0.004)

    # Mandatory anti-spoofing check: >2km jump in 1 minute (speed >120 km/h) is impossible.
    fraud_bias = float(worker.get("fraud_flags", 0.03))
    forced_jump = rnd.random() < _bounded(0.05 + (fraud_bias * 2.5), 0.05, 0.5)
    distance_km = rnd.uniform(2.2, 5.5) if forced_jump else rnd.uniform(0.08, 1.7)
    bearing = rnd.uniform(0, 360)

    curr_lat, curr_lon = _offset_point(prev_lat, prev_lon, distance_km, bearing)
    jump_km = _haversine_km(prev_lat, prev_lon, curr_lat, curr_lon)
    delta_minutes = 1.0
    speed_kmph = jump_km / (delta_minutes / 60)
    impossible_velocity_flag = jump_km > 2.0 and speed_kmph > 120.0

    speed_validation = _bounded(1 - max(0.0, speed_kmph - 120.0) / 160.0)
    location_consistency = _bounded(1 - min(jump_km / 6.0, 1.0))

    return {
        "location_consistency": location_consistency,
        "speed_validation": speed_validation,
        "jump_km": round(jump_km, 4),
        "speed_kmph": round(speed_kmph, 3),
        "impossible_velocity_flag": impossible_velocity_flag,
    }


async def calculate_fraud_risk(
    db: AsyncIOMotorDatabase,
    worker: dict[str, Any],
    disruption: dict[str, Any],
    expected_orders: float,
    actual_orders: float,
) -> dict[str, Any]:
    worker_id = str(worker["_id"])
    disruption_id = str(disruption["_id"])
    rnd = _rnd(worker_id, disruption_id)

    base_fraud = float(worker.get("fraud_flags", 0.03))
    velocity_signal = _simulate_velocity_signal(worker, rnd)

    location_consistency = _bounded(
        (float(velocity_signal["location_consistency"]) * 0.8) + ((1 - base_fraud) * 0.2) - rnd.uniform(0.0, 0.1)
    )
    speed_validation = _bounded(min(float(velocity_signal["speed_validation"]), 1 - (base_fraud * 0.25)))
    ip_gps_mismatch = _bounded((base_fraud * 0.8) + rnd.uniform(0.03, 0.4))

    if expected_orders <= 0:
        activity_mismatch = 0.0
    else:
        activity_mismatch = _bounded(abs(expected_orders - actual_orders) / expected_orders)

    two_weeks_ago = utc_now() - timedelta(days=14)
    historical_claim_spike = await db.claims.count_documents(
        {
            "worker_id": worker_id,
            "created_at": {"$gte": two_weeks_ago},
            "status": {"$in": ["approved", "under_review", "blocked"]},
        }
    )
    historical_anomaly = _bounded(historical_claim_spike / 10)

    location_risk = 1 - location_consistency
    device_risk = 1 - speed_validation
    impossible_velocity_risk = 1.0 if bool(velocity_signal["impossible_velocity_flag"]) else 0.0

    fraud_risk_score = _bounded(
        (0.24 * location_risk)
        + (0.16 * device_risk)
        + (0.16 * ip_gps_mismatch)
        + (0.18 * activity_mismatch)
        + (0.1 * historical_anomaly)
        + (0.16 * impossible_velocity_risk)
    )

    if impossible_velocity_risk and fraud_risk_score < 0.72:
        # Velocity spoofing must always trigger review or block.
        fraud_risk_score = 0.72

    signals = {
        "LocationConsistency": round(location_consistency, 4),
        "SpeedValidation": round(speed_validation, 4),
        "IPvsGPSMismatch": round(ip_gps_mismatch, 4),
        "ActivityMismatch": round(activity_mismatch, 4),
        "HistoricalAnomaly": round(historical_anomaly, 4),
        "LocationJumpKm": float(velocity_signal["jump_km"]),
        "SpeedKmph": float(velocity_signal["speed_kmph"]),
        "ImpossibleVelocityFlag": bool(velocity_signal["impossible_velocity_flag"]),
    }

    return {
        "fraud_risk_score": round(fraud_risk_score, 4),
        "signals": signals,
        "impossible_velocity_flag": bool(velocity_signal["impossible_velocity_flag"]),
    }
