import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cerebras.cloud.sdk import Cerebras
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
cerebras = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))
HF_TOKEN = os.getenv("HF_API_TOKEN")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

class Prompt(BaseModel):
    prompt: str

def measure(fn, *args, **kwargs):
    """Utility to measure execution time"""
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

@app.get("/")
def home():
    return {"message": "SpeedGPT backend is running 🚀"}

@app.post("/api/cerebras")
def cerebras_api(p: Prompt):
    def call():
        return cerebras.chat.completions.create(
            messages=[{"role": "user", "content": p.prompt}],
            model="llama-4-scout-17b-16e-instruct",
        )
    out, elapsed = measure(call)
    text = out.get("message", out)
    return {"provider": "Cerebras", "latency": round(elapsed, 3), "response": str(text)}

@app.post("/api/huggingface")
def huggingface_api(p: Prompt):
    def call():
        payload = {"inputs": p.prompt}
        res = requests.post(
            "https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-chat-hf",
            headers=HF_HEADERS,
            json=payload,
            timeout=120
        )
        res.raise_for_status()
        return res.json()
    out, elapsed = measure(call)
    return {"provider": "HuggingFace", "latency": round(elapsed, 3), "response": str(out)}

@app.post("/api/compare")
def compare(p: Prompt):
    cerebras_out, cerebras_time = measure(lambda: cerebras.chat.completions.create(
        messages=[{"role": "user", "content": p.prompt}],
        model="llama-4-scout-17b-16e-instruct"
    ))
    hf_out, hf_time = measure(lambda: requests.post(
        "https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-chat-hf",
        headers=HF_HEADERS,
        json={"inputs": p.prompt}
    ).json())
    return {
        "cerebras": {"latency": round(cerebras_time, 3), "response": str(cerebras_out)},
        "huggingface": {"latency": round(hf_time, 3), "response": str(hf_out)},
    }

@app.post("/generate")
def generate(p: Prompt):
    """Default endpoint used by frontend (Cerebras by default)."""
    try:
        response = cerebras.chat.completions.create(
            messages=[{"role": "user", "content": p.prompt}],
            model="llama-4-scout-17b-16e-instruct"
        )

        # Extract the human-readable reply
        text = response.choices[0].message.content

        return {"response": text}
    except Exception as e:
        return {"error": str(e)}
