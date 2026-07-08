from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from server.database import get_db
from server.models import User
from server.schemas import UserCreate, UserResponse
from server.auth import hash_password, get_current_user, require_admin

router = APIRouter(prefix="/api/users", tags=["User Management"])


@router.get("", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).all()


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete admin")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}