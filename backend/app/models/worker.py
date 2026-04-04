from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Platform = Literal["Blinkit", "Zepto", "Instamart"]


class WorkerProfileInput(BaseModel):
    name: str
    age: int = Field(ge=18, le=65)
    phone: str = Field(min_length=10, max_length=15)
    delivery_platform: Platform
    worker_id: str
    city: str
    state: str
    zone: str
    weekly_income: float = Field(gt=0)
    experience_months: int = Field(ge=0)
    avg_orders_per_hour: float = Field(gt=0)
    working_hours_per_day: float = Field(gt=0, le=16)
    gps_permission: bool
    upi_id: str


class WorkerRegistrationRequest(WorkerProfileInput):
    otp: str = Field(min_length=6, max_length=6)


class WorkerLoginRequest(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    otp: str = Field(min_length=6, max_length=6)


class WorkerActivityPatch(BaseModel):
    completed_orders: int = Field(ge=0)
    assigned_orders: int = Field(ge=1)
    weekly_working_hours: float = Field(gt=0)


class WorkerResponse(BaseModel):
    id: str
    name: str
    age: int
    phone: str
    delivery_platform: Platform
    worker_id: str
    city: str
    state: str
    zone: str
    weekly_income: float
    experience_months: int
    avg_orders_per_hour: float
    working_hours_per_day: float
    gps_permission: bool
    upi_id: str
    completed_orders: int
    assigned_orders: int
    weekly_working_hours: float
    fraud_flags: float
    created_at: datetime

