from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.plan import Plan

init_db()
db = SessionLocal()

if db.query(Plan).count() == 0:
    plans = [
        Plan(name="Started", max_bots=1, email_alerts=False, api_access=False, backtesting=False, price=0),
        Plan(name="Pro", max_bots=5, email_alerts=True, api_access=False, backtesting=True, price=6),
        Plan(name="Elite", max_bots=-1, email_alerts=True, api_access=True, backtesting=True, price=35),
    ]
    db.add_all(plans)
    db.commit()
    print("Plans insérés ✅")
else:
    print("Plans déjà présents ✅")

db.close()