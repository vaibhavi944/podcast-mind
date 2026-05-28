import pandas as pd
from typing import List, Dict, Optional
from backend.engines.semantic_engine import SemanticEngine
from backend.engines.collaborative_engine import CollaborativeEngine
from backend.models.schemas import PodcastResult
from backend.config import settings

class HybridEngine:
    """
    The orchestration brain of PodcastMind.
    Combines semantic and collaborative signals into a unified ranking.
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.collab_engine = CollaborativeEngine()

    def recommend(
        self, 
        query: Optional[str] = None, 
        podcast_id: Optional[str] = None, 
        limit: int = 5,
        s_weight: float = 0.7,
        c_weight: float = 0.3
    ) -> List[PodcastResult]:
        """
        Core hybrid recommendation logic:
        1. Retrieval
        2. Normalization
        3. Blending
        4. Explanation
        """
        
        # 1. Retrieval Phase
        semantic_pool = self.semantic_engine.get_candidates(query) if query else {}
        collab_pool = self.collab_engine.get_candidates(podcast_id) if podcast_id else {}
        
        if not semantic_pool and not collab_pool:
            return []

        # 2. Normalization Phase (Min-Max)
        semantic_pool = self._normalize(semantic_pool, 'semantic_score')
        collab_pool = self._normalize(collab_pool, 'collaborative_score')

        # 3. Merging & Blending
        all_ids = set(semantic_pool.keys()) | set(collab_pool.keys())
        blended_results = []

        for pid in all_ids:
            # Get base metadata
            meta = semantic_pool.get(pid, collab_pool.get(pid))['metadata']
            
            # Handle potential NaN categories or missing fields
            categories = meta.get('categories', 'General')
            if pd.isna(categories):
                categories = 'General'

            s_score = semantic_pool.get(pid, {}).get('norm_semantic_score', 0.0)
            c_score = collab_pool.get(pid, {}).get('norm_collaborative_score', 0.0)
            
            # Weighted Blend
            blended_score = (s_score * s_weight) + (c_score * c_weight)
            
            result = PodcastResult(
                podcast_id=pid,
                title=meta['title'],
                categories=categories,
                semantic_score=s_score,
                collaborative_score=c_score,
                blended_score=blended_score
            )
            
            # 4. Explanation Phase
            result.explanation = self._generate_explanation(result)
            blended_results.append(result)

        # 5. Ranking & Deduplication
        # Sort by blended score descending
        blended_results.sort(key=lambda x: x.blended_score, reverse=True)
        
        # Remove target podcast if present
        if podcast_id:
            blended_results = [r for r in blended_results if r.podcast_id != podcast_id]
            
        return blended_results[:limit]

    def _normalize(self, pool: Dict, score_key: str) -> Dict:
        if not pool: return pool
        
        scores = [c[score_key] for c in pool.values()]
        min_s, max_s = min(scores), max(scores)
        
        diff = max_s - min_s
        for pid in pool:
            raw = pool[pid][score_key]
            pool[pid][f'norm_{score_key}'] = (raw - min_s) / diff if diff > 0 else 1.0
            
        return pool

    def _generate_explanation(self, result: PodcastResult) -> str:
        """Heuristic-based explanation logic."""
        if result.semantic_score > 0.8 and result.collaborative_score > 0.8:
            return "A top-tier match! Both content and community behavior strongly support this show."
        elif result.semantic_score > result.collaborative_score:
            main_cat = result.categories.split(',')[0]
            return f"Highly relevant to your interests in {main_cat}."
        else:
            return "Popular among listeners with similar tastes to yours."
