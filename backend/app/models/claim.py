from datetime import datetime
from pydantic import BaseModel


class ClaimResponse(BaseModel):
    id: str
    worker_id: str
    disruption_id: str
    policy_id: str
    status: str
    duration_hours: float
    severity: float
    expected_orders: float
    actual_orders: float
    work_loss_ratio: float
    fraud_risk_score: float
    payout_amount: float
    payout_message: str | None = None
    payout_txn_id: str | None = None
    reason: str | None = None
    created_at: datetime


class FraudLogResponse(BaseModel):
    id: str
    worker_id: str
    claim_id: str | None = None
    fraud_risk_score: float
    action: str
    signals: dict
    created_at: datetime

