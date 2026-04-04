import random
from typing import Any

from app.utils.time import utc_now


DISRUPTION_WEIGHTS: dict[str, float] = {
    "rain": 0.13,
    "flood": 0.11,
    "traffic": 0.14,
    "heat": 0.09,
    "pollution": 0.08,
    "curfew": 0.09,
    "strike": 0.09,
    "store_outage": 0.1,
    "server_outage": 0.09,
    "power_outage": 0.08,
}


def _bounded(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def _build_zone_baseline(worker: dict[str, Any]) -> dict[str, float]:
    seed = f"{worker.get('city', 'Unknown')}:{worker.get('zone', 'Unknown')}:{utc_now().date()}"
    rnd = random.Random(seed)

    return {
        "total_days": 30,
        "time_period": 30,
        "rainy_days": rnd.randint(5, 17),
        "flood_events": rnd.randint(0, 6),
        "congestion_hours": rnd.uniform(10, 45),
        "heatwave_days": rnd.randint(2, 13),
        "aqi_bad_days": rnd.randint(4, 20),
        "curfew_hours": rnd.uniform(0, 10),
        "strike_hours": rnd.uniform(0, 14),
        "store_outage_hours": rnd.uniform(2, 24),
        "server_outage_hours": rnd.uniform(1, 16),
        "power_outage_hours": rnd.uniform(2, 20),
    }


def calculate_risk_profile(worker: dict[str, Any], zone_inputs: dict[str, float] | None = None) -> dict[str, Any]:
    inputs = zone_inputs or _build_zone_baseline(worker)

    max_weekly_hours = max(worker.get("working_hours_per_day", 8) * 7, 1)

    probabilities = {
        "rain": _bounded(_safe_div(inputs["rainy_days"], inputs["total_days"])),
        "flood": _bounded(_safe_div(inputs["flood_events"], inputs["time_period"])),
        "traffic": _bounded(_safe_div(inputs["congestion_hours"], max_weekly_hours)),
        "heat": _bounded(_safe_div(inputs["heatwave_days"], inputs["total_days"])),
        "pollution": _bounded(_safe_div(inputs["aqi_bad_days"], inputs["total_days"])),
        "curfew": _bounded(_safe_div(inputs["curfew_hours"], 168)),
        "strike": _bounded(_safe_div(inputs["strike_hours"], 168)),
        "store_outage": _bounded(_safe_div(inputs["store_outage_hours"], max_weekly_hours)),
        "server_outage": _bounded(_safe_div(inputs["server_outage_hours"], 168)),
        "power_outage": _bounded(_safe_div(inputs["power_outage_hours"], 168)),
    }

    raw_risk_score = sum(probabilities[key] * DISRUPTION_WEIGHTS[key] for key in DISRUPTION_WEIGHTS)
    normalized_risk_score = min(1.0, raw_risk_score)
    exposure_score = sum(probabilities.values()) / len(probabilities)

    weekly_working_hours = worker.get("weekly_working_hours", max_weekly_hours * 0.8)
    completed_orders = worker.get("completed_orders", 80)
    assigned_orders = max(worker.get("assigned_orders", 100), 1)
    experience_months = worker.get("experience_months", 0)
    fraud_flags = _bounded(worker.get("fraud_flags", 0.03), 0.0, 1.0)

    activity_score = _bounded(_safe_div(weekly_working_hours, max_weekly_hours))
    completion_score = _bounded(_safe_div(completed_orders, assigned_orders))
    work_history_score = _bounded(min(experience_months / 24, 1))
    fraud_score = _bounded(1 - fraud_flags)

    reliability_score = (activity_score + completion_score + work_history_score + fraud_score) / 4

    return {
        "probabilities": {key: round(value, 4) for key, value in probabilities.items()},
        "weights": DISRUPTION_WEIGHTS,
        "risk_score": round(_bounded(normalized_risk_score), 4),
        "raw_risk_score": round(raw_risk_score, 4),
        "exposure_score": round(_bounded(exposure_score), 4),
        "reliability_score": round(_bounded(reliability_score), 4),
        "reliability_breakdown": {
            "activity_score": round(activity_score, 4),
            "completion_score": round(completion_score, 4),
            "work_history_score": round(work_history_score, 4),
            "fraud_score": round(fraud_score, 4),
        },
        "raw_inputs": inputs,
    }

