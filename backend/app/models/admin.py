from pydantic import BaseModel


class AdminMetricsResponse(BaseModel):
    total_workers: int
    active_policies: int
    total_premium_collected: float
    total_payouts: float
    loss_ratio: float
    fraud_alerts: int
    active_disruptions: int


class MonitoringRunResponse(BaseModel):
    zones_checked: int
    disruptions_detected: int
    claims_generated: int
    approved_claims: int
    blocked_claims: int
    review_claims: int

