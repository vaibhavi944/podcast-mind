from pydantic import BaseModel, Field
from typing import List, Optional

class PodcastResult(BaseModel):
    """Schema for a single podcast recommendation result."""
    podcast_id: str
    title: str
    author: Optional[str] = None
    categories: str
    semantic_score: float = 0.0
    collaborative_score: float = 0.0
    blended_score: float = 0.0
    explanation: Optional[str] = None

class RecommendationRequest(BaseModel):
    """Schema for incoming recommendation requests."""
    query: Optional[str] = Field(None, description="Natural language search query")
    podcast_id: Optional[str] = Field(None, description="Target podcast ID for similar shows")
    limit: int = Field(5, ge=1, le=20, description="Number of recommendations to return")
    semantic_weight: float = Field(0.7, ge=0.0, le=1.0)
    collaborative_weight: float = Field(0.3, ge=0.0, le=1.0)
    preferred_categories: Optional[List[str]] = Field(None, description="User's preferred categories for boosting")

class RecommendationResponse(BaseModel):
    """Schema for standardized API response."""
    status: str = "success"
    count: int
    results: List[PodcastResult]
    metadata: Optional[dict] = None
