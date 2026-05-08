from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.plan import Plan
import app.models.user
import app.models.bot
import app.models.trade
import app.models.news
import app.models.signal


def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Insérer les plans si pas encore présents
    db = SessionLocal()
    try:
        if db.query(Plan).count() == 0:
            plans = [
                Plan(name="Started", max_bots=1, email_alerts=False, api_access=False, backtesting=False, price=0),
                Plan(name="Pro", max_bots=5, email_alerts=True, api_access=False, backtesting=True, price=6),
                Plan(name="Elite", max_bots=-1, email_alerts=True, api_access=True, backtesting=True, price=35),
            ]
            db.add_all(plans)
            db.commit()
    finally:
        db.close()