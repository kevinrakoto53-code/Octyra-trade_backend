from app.workers.celery_app import celery_app
from app.db.session import SessionLocal

import app.models.user
import app.models.plan
import app.models.bot
import app.models.trade
import app.models.news
import app.models.signal

from app.models.bot import Bot
from app.models.trade import Trade
from app.models.user import User
from app.services.market_service import get_price
from app.services.ml_service import get_signal
from app.services.trading_service import execute_trade
from app.services.email_service import send_trade_alert
import asyncio
import logging
logger = logging.getLogger(__name__)

@celery_app.task
def run_bot_cycle(bot_id: int):
    db = SessionLocal()
    try:
        bot = db.query(Bot).filter(Bot.id == bot_id).first()
        if not bot or bot.status != "active":
            return

        signal = get_signal(bot.asset)
        
        # si erreur dans le signal on arrête proprement
        if not signal or "error" in signal:
            logger.warning(f"Signal indisponible pour {bot.asset}: {signal}")
            return

        final_decision = signal.get("final_decision", "HOLD")
        logger.warning(f">>> Décision: {final_decision}")

        if final_decision == "HOLD":
            return

        price_data = get_price(bot.asset)
        if not price_data or "error" in price_data:
            logger.warning(f"Prix indisponible pour {bot.asset}")
            return

        price = price_data.get("price", 0)
        trade_result = execute_trade(bot.asset, final_decision)

        trade = Trade(
            bot_id=bot.id,
            asset=bot.asset,
            action=final_decision,
            price=price,
            quantity=0.001,
            rf_signal=signal.get("rf_signal"),
            xgb_signal=signal.get("xgb_signal"),
            final_decision=final_decision,
        )
        db.add(trade)
        db.commit()
        logger.warning(f">>> Trade sauvegardé: {final_decision} {bot.asset} @ {price}")

        if bot.email_alert:
            user = db.query(User).filter(User.id == bot.user_id).first()
            if user:
                asyncio.run(send_trade_alert(
                    to_email=user.email,
                    asset=bot.asset,
                    action=final_decision,
                    price=price,
                    bot_name=bot.name
                ))

    except Exception as e:
        logger.error(f"Erreur bot {bot_id}: {e}", exc_info=True)
    finally:
        db.close()


import time

@celery_app.task
def run_all_active_bots():
    db = SessionLocal()
    try:
        active_bots = db.query(Bot).filter(Bot.status == "active").all()
        for bot in active_bots:
            run_bot_cycle.delay(bot.id)
            time.sleep(2)  # 2 secondes entre chaque bot
        print(f"{len(active_bots)} bots lancés ✅")
    finally:
        db.close()