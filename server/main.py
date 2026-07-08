"""InfraPilot — Main Application Entry Point."""

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from server.database import init_db, SessionLocal
from server.config import get_settings
from server.schemas import DashboardSummary
from server.models import System, MetricRecord, Alert
from server.auth import create_default_admin

from server.routers import (
    auth as auth_router,
    systems as systems_router,
    metrics as metrics_router,
    alerts as alerts_router,
    users as users_router,
)

app = FastAPI(
    title="InfraPilot API",
    description="Enterprise Infrastructure Monitoring & Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router.router)
app.include_router(systems_router.router)
app.include_router(metrics_router.router)
app.include_router(alerts_router.router)
app.include_router(users_router.router)


@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    try:
        create_default_admin(db)
    finally:
        db.close()


@app.get("/", tags=["Root"])
def root():
    return {
        "name": "InfraPilot",
        "version": "1.0.0",
        "docs": "/docs",
        "dashboard": "/dashboard",
    }


@app.get("/api/dashboard/summary", response_model=DashboardSummary, tags=["Dashboard"])
def dashboard_summary():
    db = SessionLocal()
    try:
        total = db.query(System).count()
        active = db.query(System).filter(System.status == "active").count()
        alerts_total = db.query(Alert).filter(Alert.acknowledged == False).count()
        critical = db.query(Alert).filter(Alert.severity == "critical", Alert.acknowledged == False).count()

        avg_cpu = db.query(MetricRecord).order_by(MetricRecord.timestamp.desc()).first()
        return DashboardSummary(
            total_systems=total,
            active_systems=active,
            total_alerts=alerts_total,
            critical_alerts=critical,
            avg_cpu=avg_cpu.cpu_percent if avg_cpu else 0,
            avg_memory=avg_cpu.memory_percent if avg_cpu else 0,
            avg_disk=avg_cpu.disk_percent if avg_cpu else 0,
        )
    finally:
        db.close()


@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard"])
def get_dashboard():
    """Serve the web dashboard."""
    dashboard_path = Path(__file__).parent.parent / "dashboard" / "index.html"
    if not dashboard_path.exists():
        return HTMLResponse("<h1>Dashboard not found</h1><p>Build dashboard first.</p>", status_code=404)
    return HTMLResponse(dashboard_path.read_text())


if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)