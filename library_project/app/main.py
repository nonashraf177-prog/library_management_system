# app/main.py
# Run with: python -m uvicorn app.main:app --reload

from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.logging_config import setup_logging
from app.models import user_model, book_model, borrow_model          # noqa: F401
from app.routes import auth_routes, book_routes, borrow_routes, user_routes
from app.monitoring.dashboard_routes import router as monitoring_router
from app.middleware.logging_middleware import RequestLoggingMiddleware

# ── Initialise logging first ─────────────────────────────────────────────────
setup_logging()

# ── Create DB tables ─────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Library Management System",
    description="REST API for managing a library — books, users, borrowing.",
    version="1.0.0",
)

# ── Middleware ────────────────────────────────────────────────────────────────
app.add_middleware(RequestLoggingMiddleware)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(book_routes.router)
app.include_router(borrow_routes.router)
app.include_router(monitoring_router)


@app.get("/", tags=["Root"])
def read_root():
    return {"status": "Library Management System is running!"}
