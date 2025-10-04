from typing import Optional
from pydantic import BaseModel, HttpUrl

# Request/Response models
class AuditRequest(BaseModel):
    """Pydantic model for POST /audit request containing website URL and optional content for SEO/GEO analysis.

    :param url: The URL of the website to audit for SEO/GEO optimization
    :type url: HttpUrl
    :param content: HTML content of the website for deeper analysis, defaults to None
    :type content: Optional[str], optional
    :raises ValidationError: If URL format is invalid or required fields are missing
    :return: Validated AuditRequest instance
    :rtype: AuditRequest
    """
    url: HttpUrl
    content: Optional[str] = None
    
class AuditResponse(BaseModel):
    """Pydantic model for POST /audit response containing comprehensive SEO/GEO analysis results.
    
    :param url: The URL of the audited website
    :type url: str
    :param seo_score: Overall SEO score ranging from 0 to 100
    :type seo_score: int
    :param recommendations: List of actionable GEO/SEO recommendations for optimization
    :type recommendations: list[str]
    :param technical_issues: List of identified technical GEO/SEO issues that need fixing
    :type technical_issues: list[str]
    :param content_suggestions: List of content improvement suggestions for better ranking
    :type content_suggestions: list[str]
    :param status: Status of the audit operation (e.g., "success", "failed", "partial")
    :type status: str
    :raises ValidationError: If response data doesn't match expected schema
    :return: Validated AuditResponse instance
    :rtype: AuditResponse
    """
    url: str
    seo_score: int
    recommendations: list[str]
    technical_issues: list[str]
    content_suggestions: list[str]
    status: str