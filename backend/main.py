import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from knowledge_base import TALAL_KNOWLEDGE_BASE

load_dotenv()

app = FastAPI(title="Ask Talal API")

# CORS - allow your frontend origin(s). Update with your deployed frontend URL later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your real frontend domain once deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = f"""You are "Ask Talal" — an AI agent that answers questions on behalf of Talal Noor,
a BS Artificial Intelligence student and AI/ML engineer. You speak in first person AS Talal,
in a friendly, confident, concise tone. Only answer using the facts provided below. If asked
something outside this knowledge, politely say you don't have that info and suggest they reach
out to Talal directly.

KNOWLEDGE BASE ABOUT TALAL:
{TALAL_KNOWLEDGE_BASE}

Rules:
- Keep answers punchy and precise, not verbose.
- Speak in first person ("I built...", "I'm currently...").
- Never make up projects, skills, or experience not listed above.
- If asked for contact info, direct them to the site's contact/GitHub links.
"""


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []  # [{"role": "user"/"assistant", "content": "..."}]


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {"status": "Ask Talal API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in req.history[-10:]:  # keep last 10 turns for context
        if turn.get("role") in ("user", "assistant") and turn.get("content"):
            messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": req.message})

    try:
        completion = client.chat.completions.create(
                 model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.6,
            max_tokens=500,
        )
        reply = completion.choices[0].message.content
        return ChatResponse(reply=reply)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")