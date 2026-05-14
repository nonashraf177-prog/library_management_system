# app/middleware/logging_middleware.py
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.monitoring.metrics import record_request

logger = logging.getLogger("library_app")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every HTTP request with method, path, status code, and duration.
    Also feeds data into the in-memory metrics store.
    """

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                f"Unhandled exception | {request.method} {request.url.path} | {exc}",
                exc_info=True,
            )
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        status = response.status_code

        logger.info(
            f"{request.method} {request.url.path} -> {status} ({duration_ms} ms)"
        )

        # Feed into metrics
        record_request(
            path=request.url.path,
            method=request.method,
            status=status,
            duration=duration_ms,
        )

        return response
