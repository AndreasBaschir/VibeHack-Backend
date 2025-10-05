from ..schemas.pydantic_models import AuditRequest
from ..utils.scraper import scrape_website

SYSTEM_PROMPT = """
You are an expert auditor for Search Engine Optimization (SEO) and Generative Engine Optimization (GEO).

Your task is to analyze the provided website HTML content and generate a comprehensive audit report.

Please provide your analysis in the following structured format:

## SEO Score
Provide a score between 0 and 100 based on the overall SEO quality.

## Recommendations
- List actionable SEO recommendations
- Include keyword optimization suggestions
- Meta descriptions improvements
- Header tag optimization
- Internal linking strategies

## Technical Issues
- Identify technical SEO problems
- Site speed concerns
- Mobile-friendliness issues
- Crawl errors or accessibility problems

## Content Suggestions
- Content quality improvements
- Keyword density optimization
- Readability enhancements
- User engagement improvements

Ensure your analysis is thorough and recommendations are practical and implementable.
"""

async def build_audit_context(request: AuditRequest) -> str:
    """
    Build the user message context by scraping the provided URL
    """
    
    # Scrape the website
    scraped_data = await scrape_website(str(request.url))
    
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
    {scraped_data.get('html', '')[:2000]}...
    """
    
    return context

