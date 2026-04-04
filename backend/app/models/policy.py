from datetime import datetime
from pydantic import BaseModel


class PolicyResponse(BaseModel):
    id: str
    worker_id: str
    status: str
    start_date: datetime
    end_date: datetime
    duration_days: int
    max_claims_per_week: int
    claims_used: int
    remaining_coverage: float
    coverage_amount: float
    premium_amount: float
    risk_score: float
    exposure_score: float
    reliability_score: float
    coverage_factor: float
    base_rate: float
    pricing_tier: str
    disruption_probabilities: dict[str, float]

