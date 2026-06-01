from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.loader import artifacts
from backend.config import settings
from backend.engines.hybrid_engine import HybridEngine
from backend.models.schemas import RecommendationResponse, PodcastResult
from typing import Optional, List

app = FastAPI(title=settings.APP_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
hybrid_engine = None

@app.on_event("startup")
async def startup_event():
    """
    Initializes the backend foundation.
    Loads AI artifacts into memory once at startup for high-performance inference.
    """
    global hybrid_engine
    print(f"Starting {settings.APP_NAME}...")
    artifacts.load_all()
    hybrid_engine = HybridEngine()
    print("Backend ready.")

@app.get("/health")
async def health_check():
    """Health check endpoint for production monitoring."""
    return {
        "status": "online",
        "version": "1.0.0",
        "artifacts_loaded": artifacts.faiss_index is not None
    }

@app.get("/recommend", response_model=RecommendationResponse)
async def recommend(
    query: Optional[str] = None,
    podcast_id: Optional[str] = None,
    limit: int = 5,
    semantic_weight: float = 0.7,
    collaborative_weight: float = 0.3,
    preferred_categories: Optional[List[str]] = Query(None)
):
    """
    Unified hybrid recommendation endpoint.
    Accepts natural language query and/or a podcast ID.
    Supports user personalization via 'preferred_categories'.
    """
    if not query and not podcast_id:
        raise HTTPException(status_code=400, detail="Either 'query' or 'podcast_id' must be provided.")

    try:
        results = hybrid_engine.recommend(
            query=query,
            podcast_id=podcast_id,
            limit=limit,
            s_weight=semantic_weight,
            c_weight=collaborative_weight,
            preferred_categories=preferred_categories
        )
        return RecommendationResponse(
            count=len(results),
            results=results,
            metadata={"query": query, "podcast_id": podcast_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/similar", response_model=RecommendationResponse)
async def similar(podcast_id: str, limit: int = 5):
    """
    Returns behaviorally similar podcasts for a given show.
    """
    try:
        # For 'similar', we primarily use collaborative weight but keep some semantic signal
        results = hybrid_engine.recommend(
            podcast_id=podcast_id,
            limit=limit,
            s_weight=0.2,
            c_weight=0.8
        )
        return RecommendationResponse(
            count=len(results),
            results=results,
            metadata={"podcast_id": podcast_id, "type": "similar"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search", response_model=RecommendationResponse)
async def search(
    query: str, 
    limit: int = 5,
    preferred_categories: Optional[List[str]] = Query(None)
):
    """
    Pure semantic search endpoint.
    Supports user personalization via 'preferred_categories'.
    """
    try:
        # For 'search', we rely entirely on semantic retrieval
        results = hybrid_engine.recommend(
            query=query,
            limit=limit,
            s_weight=1.0,
            c_weight=0.0,
            preferred_categories=preferred_categories
        )
        return RecommendationResponse(
            count=len(results),
            results=results,
            metadata={"query": query, "type": "search"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
