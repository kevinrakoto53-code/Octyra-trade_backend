from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

GROQ_MODEL = "llama-3.1-8b-instant"


async def analyze_sentiment(title: str, content: str) -> dict:
    prompt = f"""
    Analyze the sentiment of this financial news and return ONLY a JSON object.
    
    Title: {title}
    Content: {content}
    
    Return exactly this JSON format:
    {{
        "sentiment": "positive" or "negative" or "neutral",
        "impact": a float between -1.0 and 1.0,
        "explanation": "one short sentence explaining why"
    }}
    
    Return ONLY the JSON, no other text.
    """

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200,
        )
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"sentiment": "neutral", "impact": 0.0, "explanation": str(e)}


async def chat_response(message: str, history: list = []) -> str:
    messages = [
        {
            "role": "system",
            "content": """You are OCTYRA's AI assistant, an intelligent trading platform. 
            Help users understand trading, market analysis, and how to use the platform.
            Be concise, professional and helpful. Answer in the same language as the user."""
        }
    ]

    for msg in history:
        messages.append(msg)

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur: {str(e)}"