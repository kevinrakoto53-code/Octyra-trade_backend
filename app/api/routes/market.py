from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.api.deps import get_current_user
from app.models.user import User
from app.services.market_service import get_price, get_all_prices, get_candles
import asyncio
import json

router = APIRouter(prefix="/market", tags=["Market"])

POPULAR = ["BTC", "ETH", "SOL", "BNB", "OR", "PETROLE", "EUR", "GBP"]

@router.get("/prices")
def get_prices(current_user: User = Depends(get_current_user)):
    return get_all_prices()


@router.get("/price/{asset}")
def get_asset_price(asset: str, current_user: User = Depends(get_current_user)):
    return get_price(asset)


@router.websocket("/ws/candles/{asset}")
async def candles_websocket(
    websocket: WebSocket,
    asset: str,
    period: str = "1d",
    interval: str = "1m"
):
    await websocket.accept()
    loop = asyncio.get_event_loop()
    try:
        while True:
            candles = await loop.run_in_executor(
                None, get_candles, asset, period, interval
            )
            await websocket.send_text(json.dumps(candles))
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Candle WS erreur: {e}")


@router.websocket("/ws/price/{asset}")
async def price_websocket(websocket: WebSocket, asset: str):
    await websocket.accept()
    loop = asyncio.get_event_loop()
    try:
        while True:
            price = await loop.run_in_executor(None, get_price, asset)
            await websocket.send_text(json.dumps(price))
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Price WS erreur: {e}")

@router.get("/prices/popular")
def get_popular_prices(current_user: User = Depends(get_current_user)):
    from app.services.market_service import get_price
    return [get_price(asset) for asset in POPULAR]

@router.websocket("/ws/prices")
async def prices_websocket(websocket: WebSocket):
    await websocket.accept()
    loop = asyncio.get_event_loop()
    try:
        while True:
            prices = await loop.run_in_executor(None, get_all_prices)
            await websocket.send_text(json.dumps(prices))
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Prices WS erreur: {e}")