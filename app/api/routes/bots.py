from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user, check_plan_limit
from app.models.bot import Bot
from app.models.user import User
from app.schemas.bot import BotCreate, BotUpdate, BotResponse
from typing import List
from app.models.trade import Trade
from app.schemas.trade import TradeResponse

router = APIRouter(prefix="/bots", tags=["Bots"])


@router.post("/", response_model=BotResponse)
def create_bot(
    bot_data: BotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_plan_limit)
):
    bot = Bot(
        name=bot_data.name,
        asset=bot_data.asset,
        strategy=bot_data.strategy,
        interval=bot_data.interval,
        email_alert=bot_data.email_alert,
        user_id=current_user.id,
    )
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


@router.get("/", response_model=List[BotResponse])
def get_bots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Bot).filter(Bot.user_id == current_user.id).all()


@router.get("/{bot_id}", response_model=BotResponse)
def get_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot non trouvé")
    return bot


@router.put("/{bot_id}", response_model=BotResponse)
def update_bot(
    bot_id: int,
    bot_data: BotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot non trouvé")

    for field, value in bot_data.model_dump(exclude_unset=True).items():
        setattr(bot, field, value)

    db.commit()
    db.refresh(bot)
    return bot


@router.post("/{bot_id}/start", response_model=BotResponse)
def start_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot non trouvé")

    bot.status = "active"
    db.commit()
    db.refresh(bot)

    from app.workers.tasks import run_bot_cycle
    run_bot_cycle.delay(bot.id)

    return bot


@router.post("/{bot_id}/stop", response_model=BotResponse)
def stop_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot non trouvé")

    bot.status = "stopped"
    db.commit()
    db.refresh(bot)
    return bot


@router.delete("/{bot_id}")
def delete_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot non trouvé")

    db.delete(bot)
    db.commit()
    return {"message": "Bot supprimé ✅"}

@router.get("/{bot_id}/trades", response_model=List[TradeResponse])
def get_bot_trades(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot non trouvé")

    return db.query(Trade).filter(Trade.bot_id == bot_id).all()

@router.get("/{bot_id}/profit")
def get_bot_profit(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot non trouvé")

    trades = db.query(Trade).filter(Trade.bot_id == bot_id).order_by(Trade.executed_at).all()

    profit = 0.0
    buy_trades = []
    sell_trades = []

    for trade in trades:
        if trade.action == "BUY":
            buy_trades.append(trade.price * trade.quantity)
        elif trade.action == "SELL":
            sell_trades.append(trade.price * trade.quantity)

    pairs = min(len(buy_trades), len(sell_trades))
    for i in range(pairs):
        profit += sell_trades[i] - buy_trades[i]

    return {
        "bot_id": bot_id,
        "total_trades": len(trades),
        "buy_count": len(buy_trades),
        "sell_count": len(sell_trades),
        "completed_pairs": pairs,
        "profit": round(profit, 4),
    }