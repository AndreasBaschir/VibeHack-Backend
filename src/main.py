import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from .prompts import build_audit_context, SYSTEM_PROMPT
from .schemas import AuditRequest, AuditResponse


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("❌ GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY is required")

client = genai.Client(api_key=api_key)

logger.info("✅ GEMINI_API_KEY found, proceeding with application setup")

app = FastAPI(title="VibeHack Backend", description="AI-powered GEO analysis API", version="1.0.0")

# CORS origins for Vercel frontend
allowed_origins = [
    "http://localhost:8000",  # Local development
    "http://localhost:8080",  # Alternative local port
    "https://*.vercel.app",   # Vercel preview/production deployments
    "https://vibehack-frontend.vercel.app/",  # Main production domain (adjust as needed)
]


# Add CORS middleware for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {"message": "Welcome to the VibeHack Backend!", "version": "1.0.0"}

@app.get('/health')
def health():
    """Health check endpoint for Railway deployment"""
    return {
        "status": "healthy", 
        "service": "vibehack-backend", 
        "port": os.getenv("PORT", "8000"),
        "timestamp": "2024-01-01T00:00:00Z"  # Railway expects a timestamp
    }

@app.post('/audit', response_model=AuditResponse)
async def audit(request: AuditRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Client could not be initialized")
    
    try:
        # Scrape website and build context
        context = await build_audit_context(request)
        logger.info(f"Analyzing URL: {request.url}")
        
        # Call Gemini API
        message = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
            contents=context
        )
        
        # Parse Gemini's response
        response_text = message.text.strip()
        logger.info(f"Gemini response received: {len(response_text)} characters")
        
        # Enhanced parsing logic
        lines = response_text.split('\n')
        seo_score = 75  # Default score
        recommendations = []
        technical_issues = []
        content_suggestions = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Extract SEO score
            if "score" in line.lower() and any(char.isdigit() for char in line):
                numbers = [int(s) for s in line.split() if s.isdigit()]
                if numbers:
                    seo_score = min(100, max(0, numbers[0]))
                    
            # Detect sections
            elif "recommendation" in line.lower():
                current_section = "recommendations"
            elif "technical" in line.lower():
                current_section = "technical"
            elif "content" in line.lower() and "suggestions" in line.lower():
                current_section = "content"
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                item = line[1:].strip()
                if current_section == "recommendations":
                    recommendations.append(item)
                elif current_section == "technical":
                    technical_issues.append(item)
                elif current_section == "content":
                    content_suggestions.append(item)
        
        # Fallback recommendations if parsing failed
        if not any([recommendations, technical_issues, content_suggestions]):
            recommendations = [
                "Improve meta descriptions for better CTR",
                "Add proper heading structure (H1, H2, H3)",
                "Optimize images with descriptive alt text",
                "Improve internal linking structure"
            ]
        
        return AuditResponse(
            url=str(request.url),
            seo_score=seo_score,
            recommendations=recommendations,
            technical_issues=technical_issues,
            content_suggestions=content_suggestions,
            status="success"
        )

    except Exception as e:
        logger.error(f"Error during audit: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    logger.info(f"🚀 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
