from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime
from server.database import get_db
from server.models import System, MetricRecord, Alert, AlertConfig, User
from server.schemas import MetricPayload, AlertResponse, AlertConfigCreate, AlertConfigResponse
from server.auth import get_current_user

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])


@router.post("/ingest")
def ingest_metrics(payload: MetricPayload, db: Session = Depends(get_db)):
    """Agent endpoint — no auth required for simplicity (use API key in production)."""
    system = db.query(System).filter(System.name == payload.system_name).first()
    if not system:
        system = System(
            name=payload.system_name,
            hostname=payload.system_name,
            status="active",
        )
        db.add(system)
        db.flush()

    # Update system metadata
    system.last_seen = datetime.datetime.utcnow()
    system.status = "active"

    # Create metric record
    metric = MetricRecord(
        system_id=system.id,
        cpu_percent=payload.cpu_percent,
        cpu_count=payload.cpu_count,
        cpu_freq_current=payload.cpu_freq_current,
        memory_total=payload.memory_total,
        memory_used=payload.memory_used,
        memory_percent=payload.memory_percent,
        disk_total=payload.disk_total,
        disk_used=payload.disk_used,
        disk_percent=payload.disk_percent,
        net_bytes_sent=payload.net_bytes_sent,
        net_bytes_recv=payload.net_bytes_recv,
        net_packets_sent=payload.net_packets_sent,
        net_packets_recv=payload.net_packets_recv,
        process_count=payload.process_count,
        load_1min=payload.load_1min,
        load_5min=payload.load_5min,
        load_15min=payload.load_15min,
    )
    db.add(metric)

    # Check alert thresholds
    configs = db.query(AlertConfig).filter(AlertConfig.enabled == True).all()
    for cfg in configs:
        value = getattr(payload, f"{cfg.metric_type}_percent", 0)
        if value > cfg.threshold:
            existing = (
                db.query(Alert)
                .filter(
                    Alert.system_id == system.id,
                    Alert.alert_type == cfg.metric_type,
                    Alert.acknowledged == False,
                    Alert.created_at > datetime.datetime.utcnow() - datetime.timedelta(minutes=cfg.cooldown_minutes),
                )
                .first()
            )
            if not existing:
                alert = Alert(
                    system_id=system.id,
                    alert_type=cfg.metric_type,
                    severity=cfg.severity,
                    metric_name=f"{cfg.metric_type}_percent",
                    metric_value=value,
                    threshold=cfg.threshold,
                    message=f"{system.name}: {cfg.metric_type.upper()} at {value:.1f}% (threshold: {cfg.threshold}%)",
                )
                db.add(alert)

    db.commit()
    return {"status": "ok", "system_id": system.id}