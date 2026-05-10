from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, users, market, news, signals, chat, bots, plans
from app.db.init_db import init_db
from app.core.yfinance_patch import patch_yfinance
from app.core.warmup import warmup_cache
import yfinance as yf
import asyncio
import os

patch_yfinance()
os.makedirs('cache', exist_ok=True)
yf.set_tz_cache_location('cache/')

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    asyncio.create_task(asyncio.to_thread(warmup_cache))
    print('Serveur pret')
    yield

app = FastAPI(title='OCTYRA API', version='1.0.0', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'],
)

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(market.router, prefix='/api')
app.include_router(news.router, prefix='/api')
app.include_router(signals.router, prefix='/api')
app.include_router(chat.router, prefix='/api')
app.include_router(bots.router, prefix='/api')
app.include_router(plans.router, prefix='/api')

@app.get('/')
def root():
    return {'message': 'OCTYRA API is running'}

@app.get('/health')
def health():
    return {'status': 'ok'}
