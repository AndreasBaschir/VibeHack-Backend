import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    logger.error("❌ ANTHROPIC_API_KEY not found in environment variables")
    raise ValueError("ANTHROPIC_API_KEY is required")

logger.info("✅ ANTHROPIC_API_KEY found, proceeding with application setup")

app = FastAPI(title="VibeHack Backend", description="AI-powered GEO analysis API", version="1.0.0")

@app.get('/')
def home():
    return {"message": "Welcome to the VibeHack Backend!", "version": "1.0.0"}

@app.get('/health')
def health():
    return {"status": "healthy", "service": "vibehack-backend"}

@app.post('/audit')
def audit():
    return {"message": "Audit endpoint ready", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
