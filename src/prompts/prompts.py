from typing import Tuple
from ..schemas.pydantic_models import AuditRequest
from ..utils.scraper import scrape_website

SYSTEM_PROMPT = """
You are an expert auditor for Search Engine Optimization (SEO) and Generative Engine Optimization (GEO).

Your task is to analyze the provided website HTML content and generate a comprehensive audit report in JSON format.

The JSON object must have the following structure:
{
  "seo_score": <an integer between 0 and 100>,
  "recommendations": ["recommendation 1", "recommendation 2", ...],
  "technical_issues": ["issue 1", "issue 2", ...],
  "content_suggestions": ["suggestion 1", "suggestion 2", ...]
}

Analyze the following aspects:
- SEO: keyword optimization, meta descriptions, header tags, internal linking.
- Technical: site speed, mobile-friendliness, crawl errors, accessibility.
- Content: quality, keyword density, readability, user engagement.

Ensure your analysis is thorough and the recommendations are practical and implementable.
Provide only the JSON object in your response, without any surrounding text or markdown.
"""

async def build_audit_context(request: AuditRequest) -> Tuple[str, str]:
    """
    Build the user message context by scraping the provided URL,
    and return both the context for the model and the raw HTML content.
    """
    
    # Scrape the website
    scraped_data = await scrape_website(str(request.url))
    html_content = scraped_data.get('html', '')
    
    context = f"""
    Website URL: {request.url}

    Title: {scraped_data.get('title', 'N/A')}

    Headings Structure:
    {chr(10).join([f"{h['tag']}: {h['text']}" for h in scraped_data.get('headings', [])])}

    Links ({len(scraped_data.get('links', []))} total):
    {chr(10).join([f"- {link['text']} ({link['href']})" for link in scraped_data.get('links', [])[:10]])}
    {'...(truncated)' if len(scraped_data.get('links', [])) > 10 else ''}

    Images ({len(scraped_data.get('images', []))} total):
    {chr(10).join([f"- Alt: '{img['alt']}' Src: {img['src']}" for img in scraped_data.get('images', [])[:5]])}
    {'...(truncated)' if len(scraped_data.get('images', [])) > 5 else ''}

    Content Paragraphs:
    {chr(10).join(scraped_data.get('paragraphs', [])[:5])}
    {'...(truncated)' if len(scraped_data.get('paragraphs', [])) > 5 else ''}

    HTML Content (first 2000 characters):
    {html_content[::]}...
    """
    
    return context, html_content

