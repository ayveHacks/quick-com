from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, disruption, policy, simulation, worker

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(worker.router, prefix="/workers", tags=["worker"])
api_router.include_router(policy.router, prefix="/policies", tags=["policy"])
api_router.include_router(disruption.router, prefix="/disruptions", tags=["disruption"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])

