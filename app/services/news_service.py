import httpx
from app.core.config import settings

FINANCIAL_KEYWORDS = [
    "bitcoin", "crypto", "forex", "gold", "oil",
    "petroleum", "market", "trading", "fed", "inflation",
    "interest rate", "stock", "economy", "dollar"
]
async def fetch_news(asset: str = None, max_articles: int = 10) -> list:
    query = asset if asset else "financial markets forex crypto"

    url = "https://newsdata.io/api/1/news"
    params = {
        "q": query,
        "language": "en",
        "category": "business,top",
        "apikey": settings.NEWSDATA_API_KEY,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            print(f"Status: {data.get('status')}, totalResults: {data.get('totalResults')}")

            articles = []
            for article in data.get("results", []):
                title = article.get("title", "").strip()
                if not title:  # ← seulement le titre est obligatoire
                    continue

                # Filtre les doublons
                if article.get("duplicate"):
                    continue

                articles.append({
                    "title": title,
                    "source": article.get("source_name", "Unknown"),
                    "url": article.get("link", ""),
                    "content": article.get("description") or "",  
                    "published_at": article.get("pubDate", ""),
                    "image_url": article.get("image_url") or "",
                })

            return articles[:max_articles]

        except httpx.HTTPStatusError as e:
            print(f"Erreur HTTP {e.response.status_code}: {e.response.text}")
            return []
        except Exception as e:
            print(f"Erreur: {type(e).__name__}: {e}")
            return []


def is_relevant_news(title: str, content: str) -> bool:
    text = (title + " " + content).lower()
    return any(keyword in text for keyword in FINANCIAL_KEYWORDS)


async def get_news_for_asset(asset: str) -> list:
    asset_queries = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "OR": "gold price",
        "PETROLE": "oil price",
        "EUR": "euro dollar forex",
        "GBP": "pound sterling forex",
    }
    query = asset_queries.get(asset.upper(), asset)
    return await fetch_news(asset=query, max_articles=5)