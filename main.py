import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import time
from google import genai 

# --- CONFIGURATION ---
GEMINI_API_KEY = "ENTER_YOUR_API_KEY_HERE" # <--- Yahan apni API Key daalein
client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

# CORS allow karna zaroori hai taaki EdgeOne se request aa sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class AetherisSuperintelligence:
    def __init__(self):
        self.model_id = "gemini-2.0-flash"

    async def process(self, query: str):
        start_time = time.perf_counter()
        try:
            # Agentic Thought Process
            thought = "Accessing Neural Grid... Surpassing Human Heuristics..."
            
            # Gemini Call
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(model=self.model_id, contents=query)
            )
            
            latency = (time.perf_counter() - start_time) * 1000
            return {
                "thought": thought,
                "result": response.text,
                "latency": f"{latency:.2f}ms"
            }
        except Exception as e:
            return {"thought": "ERROR", "result": str(e), "latency": "0ms"}

asi = AetherisSuperintelligence()

@app.post("/process")
async def handle_request(request: Request):
    data = await request.json()
    return await asi.process(data.get("query", ""))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
