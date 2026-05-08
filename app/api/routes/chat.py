from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.api.deps import get_current_user
from app.models.user import User
from app.services.groq_service import chat_response

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


@router.post("/")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    history = [{"role": m.role, "content": m.content} for m in request.history]
    response = await chat_response(request.message, history)
    return {"response": response}