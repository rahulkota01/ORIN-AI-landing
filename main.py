"""
Orin - Bioscience AI Copilot by RO Ecosystem
FastAPI Application Entry Point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from router import classify_query
from models import call_groq, call_claude, call_gemini

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Orin - Bioscience AI Copilot",
    description="A domain-specific research assistant for pharmacy students, PhD researchers, and biotech labs in India. Built by RO Ecosystem.",
    version="1.0.0",
)

# CORS middleware - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    has_image: bool = False


class ChatResponse(BaseModel):
    response: str
    model_used: str
    query_type: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "Orin is alive"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Classifies the query and routes it to the appropriate AI model.
    """
    message = request.message.strip()
    has_image = request.has_image

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Classify the query
    query_type, model_provider = classify_query(message, has_image)

    # Route to the appropriate model
    try:
        if model_provider == "gemini":
            response_text = call_gemini(message)
        elif model_provider == "claude":
            response_text = call_claude(message)
        else:
            response_text = call_groq(message)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with {model_provider}: {str(e)}",
        )

    return ChatResponse(
        response=response_text,
        model_used=model_provider,
        query_type=query_type,
    )
