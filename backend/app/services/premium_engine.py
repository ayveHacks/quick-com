from typing import Any


def compute_policy_pricing(worker: dict[str, Any], risk_profile: dict[str, Any]) -> dict[str, float | str]:
    weekly_income = float(worker["weekly_income"])
    risk_score = float(risk_profile["risk_score"])
    exposure_score = float(risk_profile["exposure_score"])
    reliability_score = float(risk_profile["reliability_score"])

    coverage_factor = 0.3 + (0.2 * reliability_score) + (0.1 * exposure_score)
    coverage_amount = weekly_income * coverage_factor

    base_rate = 0.015 + (0.02 * risk_score)
    premium = weekly_income * coverage_factor * base_rate * (1 + risk_score)

    pricing_tier = "balanced"

    if risk_score < 0.3:
        premium *= 0.88
        coverage_amount *= 1.12
        pricing_tier = "low_risk_reward"
    elif risk_score > 0.6:
        premium *= 1.18
        coverage_amount *= 1.15
        pricing_tier = "high_risk_resilience"

    return {
        "coverage_factor": round(coverage_factor, 4),
        "coverage_amount": round(max(coverage_amount, 0), 2),
        "base_rate": round(base_rate, 4),
        "premium_amount": round(max(premium, 0), 2),
        "pricing_tier": pricing_tier,
    }

