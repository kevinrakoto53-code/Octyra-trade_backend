from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ml_service import get_signal, get_all_signals

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.get("/")
def get_signals(current_user: User = Depends(get_current_user)):
    return get_all_signals()


@router.get("/{asset}")
def get_asset_signal(asset: str, current_user: User = Depends(get_current_user)):
    return get_signal(asset)