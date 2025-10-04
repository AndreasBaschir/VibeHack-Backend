from ..schemas import AuditRequest

def build_audit_prompt(request: AuditRequest) -> str:
    """
    Build a dynamic prompt based on the audit request context
    """
    
    base_prompt = """
You are an expert auditor for Search Engine Optimization (SEO) and Generative Engine Optimization (GEO). 

Your task is to analyze the provided website and generate a comprehensive audit report.

Website URL: {url}
{content_section}

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
    
    # Build content section based on whether content is provided
    if request.content:
        content_section = f"""
Website Content Analysis:
{request.content[::]}...  
        """
    else:
        content_section = """
Content: No website content provided - analyze based on URL and general best practices.
        """
    
    return base_prompt.format(
        url=str(request.url),
        content_section=content_section
    )
