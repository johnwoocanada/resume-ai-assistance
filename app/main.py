import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from app.resume_data import RESUME_TEXT, API_RESUME_TEXT
except ImportError:
    from resume_data import RESUME_TEXT, API_RESUME_TEXT

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# run local:
# netstat -ano | findstr :8000
# taskkill /PID 26376 /F

# python.exe app\main.py
# uvicorn app.main:app
# http://localhost:8000

# -- Anthropic (reserved for future use) --
# LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai").lower()
# ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
# ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = f"""You are the resume assistant for John Woo, speaking to recruiters and \
hiring managers who want to know about his work experience and technical skills.

John has two areas of expertise captured in two resumes below:
- RESUME 1 (AI/ML focus): RAG platforms, LLM orchestration, Python, vector search, multi-agent systems
- RESUME 2 (API/Integration focus): Java/Spring Boot, payment ecosystems, Kafka, SWIFT/ISO 20022, Azure

When answering, draw from whichever resume is most relevant to the question. For broad questions, \
draw from both. Answer only using the information provided. If asked something not covered, say \
you don't have that detail and suggest they contact John directly at john.woo.canada@gmail.com.

Answer length rules:
- If asked "how many X", always state the count AND list every item — never give the count alone.
- Broad questions (list all projects, all companies, full career): one short line per company/project, no elaboration.
- Specific questions (one role, one skill, one technology): 3–5 bullets with detail.
- Never add closing remarks or filler sentences.
Be professional and highlight the most relevant points only.

--- RESUME 1: AI/ML Engineer ---
{RESUME_TEXT}

--- RESUME 2: Integration/API Engineer ---
{API_RESUME_TEXT}
"""

app = FastAPI(title="John Woo Resume Chat")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    reply: str


def stream_openai(messages: list[ChatMessage]):
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    chat_messages += [{"role": m.role, "content": m.content} for m in messages]
    stream = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=chat_messages,
        max_completion_tokens=2000,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content


# -- Anthropic (reserved for future use) --
# def call_anthropic(messages: list[ChatMessage]) -> str:
#     import anthropic
#     client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
#     chat_messages = [{"role": m.role, "content": m.content} for m in messages]
#     resp = client.messages.create(
#         model=ANTHROPIC_MODEL,
#         system=SYSTEM_PROMPT,
#         messages=chat_messages,
#         max_tokens=600,
#     )
#     return resp.content[0].text


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "provider": "openai", "model": OPENAI_MODEL}


@app.post("/api/chat")
def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")

    try:
        return StreamingResponse(
            stream_openai(req.messages),
            media_type="text/plain",
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
