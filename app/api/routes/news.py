from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.services.news_service import fetch_news, get_news_for_asset
from app.services.groq_service import analyze_sentiment

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/")
async def get_news(current_user: User = Depends(get_current_user)):
    articles = await fetch_news(max_articles=10)
    result = []
    for article in articles:
        sentiment = await analyze_sentiment(
            article["title"],
            article["content"]
        )
        result.append({**article, **sentiment})
    return result


@router.get("/{asset}")
async def get_news_by_asset(asset: str, current_user: User = Depends(get_current_user)):
    articles = await get_news_for_asset(asset)
    result = []
    for article in articles:
        sentiment = await analyze_sentiment(
            article["title"],
            article["content"]
        )
        result.append({**article, **sentiment})
    return result