import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("❌ GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY is required")

logger.info("✅ GEMINI_API_KEY found, proceeding with application setup")

app = FastAPI()

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the VibeHack Backend!"

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy"}

@app.route('/audit', methods=['POST'])
def audit():
    return {"message": "Audit endpoint"}
