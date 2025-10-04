# VibeHack-Backend

## User journey

1. User enters the web platform and provides the link to his website
2. The website is then scraped by a Playwright script -> HTML, CSS, metadata 
3. Scraped data is added to Claude Code Agent knowledge base:
    1. [Request]: Audit for SEO/GEO [Response]: Semantic (copywrite etc.), syntactic recommendations
    2. Generate HTML with CSS with added recommendations
    3. Send to `htmlcsstoimage.com` to generate preview of Website with added changes
4. Show preview on client

## Tech stack

### Frontend

- NextJS

### Backend

- Playwright
- Python FastAPI
- Claude SDK

### Routes

- GET /
- GET /health
- POST /audit
