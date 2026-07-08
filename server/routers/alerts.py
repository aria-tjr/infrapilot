from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from server.database import get_db
from server.models import Alert, AlertConfig, System, User
from server.schemas import AlertResponse, AlertConfigCreate, AlertConfigResponse
from server.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("", response_model=List[AlertResponse])
def list_alerts(
    severity: Optional[str] = None,
    acknowledged: Optional[bool] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Alert).join(System, Alert.system_id == System.id)
    if severity:
        query = query.filter(Alert.severity == severity)
    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)
    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    result = []
    for a in alerts:
        result.append({
            "id": a.id,
            "system_id": a.system_id,
            "system_name": a.system.name if a.system else None,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "metric_value": a.metric_value,
            "threshold": a.threshold,
            "message": a.message,
            "acknowledged": a.acknowledged,
            "created_at": a.created_at,
        })
    return result


@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    alert.acknowledged_by = current_user.username
    db.commit()
    return {"message": "Alert acknowledged"}


@router.get("/config", response_model=List[AlertConfigResponse])
def list_alert_configs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(AlertConfig).all()


@router.post("/config", response_model=AlertConfigResponse)
def create_alert_config(
    config: AlertConfigCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    cfg = AlertConfig(**config.model_dump())
    db.add(cfg)
    db.commit()
    db.refresh(cfg)
    return cfg


@router.delete("/config/{config_id}")
def delete_alert_config(config_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    cfg = db.query(AlertConfig).filter(AlertConfig.id == config_id).first()
    if not cfg:
        raise HTTPException(status_code=404, detail="Config not found")
    db.delete(cfg)
    db.commit()
    return {"message": "Alert config deleted"}