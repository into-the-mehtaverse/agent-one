"""
Main FastAPI application for the AI agent
"""

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from agent import AIAgent
from models import ChatRequest, ChatResponse

# Load environment variables
load_dotenv()

# Initialize the agent
try:
    agent = AIAgent()
except ValueError as e:
    print(f"Warning: {e}")
    agent = None

# Create FastAPI app
app = FastAPI(
    title="AI Agent API",
    description="A simple AI agent with web search capabilities",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Agent API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes messages and handles tool calls

    Args:
        request: ChatRequest containing the message and conversation history

    Returns:
        ChatResponse with the agent's response and metadata
    """
    if agent is None:
        raise HTTPException(
            status_code=500,
            detail="AI Agent not initialized. Please set OPENAI_API_KEY environment variable."
        )

    try:
        result = agent.chat(
            user_message=request.message,
            conversation_history=request.conversation_history
        )

        return ChatResponse(
            response=result["response"],
            used_tools=result["used_tools"],
            messages=result["messages"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
