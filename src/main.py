import anthropic
import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from prompts import SYSTEM_PROMPT
from schemas import AuditRequest, AuditResponse


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    logger.error("❌ ANTHROPIC_API_KEY not found in environment variables")
    raise ValueError("ANTHROPIC_API_KEY is required")

client = anthropic.Anthropic(api_key=api_key)

logger.info("✅ ANTHROPIC_API_KEY found, proceeding with application setup")

app = FastAPI(title="VibeHack Backend", description="AI-powered GEO analysis API", version="1.0.0")

@app.get('/')
def home():
    return {"message": "Welcome to the VibeHack Backend!", "version": "1.0.0"}

@app.get('/health')
def health():
    return {"status": "healthy", "service": "vibehack-backend", "port": os.getenv("PORT", "8000")}

@app.post('/audit', response_model=AuditResponse)
def audit(request: AuditRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Client could not be initialized")
    try:
        prompt = SYSTEM_PROMPT
        
        # Call Claude API
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Parse Claude's response
        response_text = message.content[0].text
        
        # Simple parsing - you can make this more sophisticated
        lines = response_text.split('\n')
        seo_score = 75  # Default score, extract from response
        recommendations = []
        technical_issues = []
        content_suggestions = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "score" in line.lower() and any(char.isdigit() for char in line):
                # Extract score from line
                numbers = [int(s) for s in line.split() if s.isdigit()]
                if numbers:
                    seo_score = min(100, max(0, numbers[0]))
            elif "recommendation" in line.lower():
                current_section = "recommendations"
            elif "technical" in line.lower():
                current_section = "technical"
            elif "content" in line.lower():
                current_section = "content"
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                item = line[1:].strip()
                if current_section == "recommendations":
                    recommendations.append(item)
                elif current_section == "technical":
                    technical_issues.append(item)
                elif current_section == "content":
                    content_suggestions.append(item)
        
        # Ensure we have some default recommendations if parsing failed
        if not recommendations and not technical_issues and not content_suggestions:
            recommendations = [
                "Improve meta descriptions",
                "Add proper heading structure",
                "Optimize images with alt text"
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
