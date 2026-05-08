from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.user import UserResponse, UpdateProfile, UpdatePassword  # ← importés depuis schemas
from app.models.user import User
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Routes ────────────────────────────────────────────────

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/my-plan")
def get_my_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "plan":          current_user.plan.name,
        "max_bots":      current_user.plan.max_bots,
        "email_alerts":  current_user.plan.email_alerts,
        "api_access":    current_user.plan.api_access,
        "backtesting":   current_user.plan.backtesting,
        "price":         current_user.plan.price,
    }

@router.patch("/me", response_model=UserResponse)
def update_profile(
    data: UpdateProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.full_name:
        current_user.full_name = data.full_name

    if data.email:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")
        current_user.email = data.email

    db.commit()
    db.refresh(current_user)
    return current_user

@router.patch("/me/password")
def update_password(
    data: UpdatePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not pwd_context.verify(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Mot de passe actuel incorrect")

    current_user.password_hash = pwd_context.hash(data.new_password)
    db.commit()
    return {"message": "Mot de passe mis à jour ✅"}