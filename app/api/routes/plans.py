from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.plan import Plan

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/")
def get_all_plans(db: Session = Depends(get_db)):
    plans = db.query(Plan).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "max_bots": p.max_bots,
            "email_alerts": p.email_alerts,
            "api_access": p.api_access,
            "backtesting": p.backtesting,
            "price": p.price,
        }
        for p in plans
    ]


@router.post("/upgrade/{plan_id}")
def upgrade_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan non trouvé")

    if current_user.plan_id == plan_id:
        raise HTTPException(
            status_code=400,
            detail=f"Tu es déjà sur le plan {plan.name}"
        )

    current_user.plan_id = plan_id
    db.commit()
    db.refresh(current_user)

    return {
        "message": f"Plan mis à jour vers {plan.name} ✅",
        "plan": {
            "id": plan.id,
            "name": plan.name,
            "max_bots": plan.max_bots,
            "email_alerts": plan.email_alerts,
            "price": plan.price,
        }
    }


@router.get("/current")
def get_current_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(Plan).filter(Plan.id == current_user.plan_id).first()
    return {
        "current_plan": plan.name,
        "plan_id": plan.id,
        "max_bots": plan.max_bots,
        "email_alerts": plan.email_alerts,
        "api_access": plan.api_access,
        "backtesting": plan.backtesting,
        "price": plan.price,
        "bots_used": len(current_user.bots),
        "bots_remaining": plan.max_bots - len(current_user.bots) if plan.max_bots != -1 else "illimité"
    }