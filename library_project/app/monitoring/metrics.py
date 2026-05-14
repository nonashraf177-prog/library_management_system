# app/monitoring/metrics.py
"""
Lightweight in-memory metrics collector.
Collects request counts, total duration, and error counts per route.
Can be replaced with Prometheus client when needed.
"""
from collections import defaultdict
from typing import Dict, Any

# ── internal stores ──────────────────────────────────────────────────────────
_request_count:    dict = defaultdict(int)
_error_count:      dict = defaultdict(int)
_total_duration:   dict = defaultdict(float)  # ms


def record_request(path: str, method: str, status: int, duration: float) -> None:
    key = f"{method}:{path}"
    _request_count[key] += 1
    _total_duration[key] += duration
    if status >= 400:
        _error_count[key] += 1


def get_metrics() -> Dict[str, Any]:
    routes = {}
    for key, count in _request_count.items():
        routes[key] = {
            "requests":     count,
            "errors":       _error_count.get(key, 0),
            "avg_duration_ms": round(_total_duration[key] / count, 2) if count else 0,
        }
    return {"routes": routes, "total_requests": sum(_request_count.values())}


def reset_metrics() -> None:
    _request_count.clear()
    _error_count.clear()
    _total_duration.clear()
