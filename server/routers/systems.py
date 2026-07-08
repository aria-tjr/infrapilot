from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from server.database import get_db
from server.models import System, MetricRecord, Alert, User
from server.schemas import SystemResponse, MetricPayload, MetricResponse
from server.auth import get_current_user

router = APIRouter(prefix="/api/systems", tags=["Systems"])


@router.get("", response_model=List[SystemResponse])
def list_systems(
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(System)
    if status_filter:
        query = query.filter(System.status == status_filter)
    return query.order_by(System.name).all()


@router.get("/{system_id}", response_model=SystemResponse)
def get_system(system_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    system = db.query(System).filter(System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system


@router.get("/{system_id}/metrics", response_model=List[MetricResponse])
def get_system_metrics(
    system_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    system = db.query(System).filter(System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return (
        db.query(MetricRecord)
        .filter(MetricRecord.system_id == system_id)
        .order_by(MetricRecord.timestamp.desc())
        .limit(limit)
        .all()
    )


@router.get("/{system_id}/live")
def get_live_metrics(system_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    system = db.query(System).filter(System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    metric = (
        db.query(MetricRecord)
        .filter(MetricRecord.system_id == system_id)
        .order_by(MetricRecord.timestamp.desc())
        .first()
    )
    if not metric:
        return {"message": "No metrics available yet"}
    return metric