"""
Pydantic models for request and response validation
"""

from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    """Model for chat messages"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    used_tools: List[str] = []
    messages: List[ChatMessage] = []
