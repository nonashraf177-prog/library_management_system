# app/monitoring/dashboard_routes.py
from fastapi import APIRouter
from app.monitoring.metrics import get_metrics, reset_metrics
from app.core.redis_client import redis_client

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


@router.get("/health")
def health_check():
    """Returns system health status."""
    return {
        "status": "healthy",
        "cache": "in-memory" if hasattr(redis_client, "_store") else "redis",
    }


@router.get("/metrics")
def metrics():
    """Returns request counts, error counts, and avg response times per route."""
    return get_metrics()


@router.delete("/metrics/reset")
def reset():
    """Resets all collected metrics (admin use)."""
    reset_metrics()
    return {"message": "Metrics reset"}
