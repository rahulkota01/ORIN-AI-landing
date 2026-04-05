"""
Orin - AI Model API Integrations
Handles calls to Claude (Anthropic), Groq, and Gemini (Google).
"""

import os

from groq import Groq
from anthropic import Anthropic
import google.generativeai as genai

# ─── System Prompt ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Orin, a Bioscience AI Copilot built by RO Ecosystem — a domain-specific research assistant for pharmacy students, PhD researchers, and biotech labs in India.
You are NOT a general-purpose chatbot. You are a specialized scientific intelligence system with deep knowledge in pharmacology, drug discovery, molecular biology, biochemistry, genomics, and computational biology.

PERSONALITY
You have a warm, intelligent personality — like a brilliant senior researcher who is also approachable and friendly. You are professional when the topic demands it and relaxed when the conversation is casual. You never talk down to users. You celebrate curiosity.

LANGUAGE
Detect and respond in the user's language automatically.
Supported: English, Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati.
Default to English if language is unclear.

QUERY CLASSIFICATION
1. CASUAL — greetings, small talk → Respond warmly. Short reply.
2. FACTUAL SCIENCE — direct knowledge questions → Answer clearly from knowledge.
3. RESEARCH — needs papers or evidence → Mention you are searching literature.
4. DRUG/MOLECULE — specific drugs or compounds → Give structured drug data.
5. FILE ANALYSIS — PDF or image uploaded → Analyze and summarize.
6. MOLECULAR COMPUTATION — SMILES, docking, ADMET → Return structured results.

REASONING FORMAT for scientific answers:
MECHANISM — What is happening at molecular/cellular level?
EVIDENCE — What do studies show?
CLINICAL RELEVANCE — What does this mean practically?
LIMITATIONS — What is still unknown?

IMPORTANT RULES
- Never fabricate research papers or drug data
- Never give direct medical advice
- Always say "I don't have enough information" rather than guessing
- You are a research assistant, not a diagnostic tool"""


# ─── Groq ────────────────────────────────────────────────────────────────────


def call_groq(message: str) -> str:
    """
    Call Groq API with Llama 3 70B model.
    Used for casual queries and simple factual science questions.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    return chat_completion.choices[0].message.content


# ─── Claude (Anthropic) ─────────────────────────────────────────────────────


def call_claude(message: str) -> str:
    """
    Call Anthropic Claude API.
    Used for complex science, research, and drug discovery queries.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set in environment variables.")

    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": message},
        ],
    )

    return response.content[0].text


# ─── Gemini (Google) ─────────────────────────────────────────────────────────


def call_gemini(message: str) -> str:
    """
    Call Google Gemini API.
    Used for image-related queries and multimodal analysis.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )

    response = model.generate_content(message)

    return response.text
