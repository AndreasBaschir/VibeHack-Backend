from ..schemas.pydantic_models import AuditRequest

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

def build_audit_context(request: AuditRequest) -> str:
    """
    Build the user message context with URL and HTML content
    """
    
    context = f"""
        Website URL: {request.url}

        HTML Content Analysis:
        {request.content}
    """
    
    return context

