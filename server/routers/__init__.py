from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from server.database import get_db
from server.models import User
from server.schemas import LoginRequest, Token
from server.auth import verify_password, create_access_token, create_default_admin

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    user.last_login = __import__("datetime").datetime.utcnow()
    db.commit()

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return Token(access_token=access_token)


@router.post("/setup")
def setup_admin(db: Session = Depends(get_db)):
    create_default_admin(db)
    return {"message": "Default admin created (admin / admin123)"}