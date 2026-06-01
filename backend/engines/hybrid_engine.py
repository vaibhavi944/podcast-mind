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
        c_weight: float = 0.3,
        preferred_categories: Optional[List[str]] = None
    ) -> List[PodcastResult]:
        """
        Core hybrid recommendation logic:
        1. Retrieval
        2. Normalization
        3. Blending & Quality Reranking
        4. Personalization Boost
        5. Confidence Calibration
        6. Explanation
        """
        
        # 1. Retrieval Phase
        semantic_pool = self.semantic_engine.get_candidates(query) if query else {}
        collab_pool = self.collab_engine.get_candidates(podcast_id) if podcast_id else {}
        
        if not semantic_pool and not collab_pool:
            return []

        # 2. Normalization Phase (Min-Max)
        semantic_pool = self._normalize(semantic_pool, 'semantic_score')
        collab_pool = self._normalize(collab_pool, 'collaborative_score')

        # 3. Merging, Blending & Quality Reranking
        all_ids = set(semantic_pool.keys()) | set(collab_pool.keys())
        blended_results = []

        for pid in all_ids:
            # Get base metadata
            meta = semantic_pool.get(pid, collab_pool.get(pid))['metadata']
            
            # Handle potential NaN categories or missing fields
            categories = meta.get('categories', 'General')
            if pd.isna(categories):
                categories = 'General'
            
            author = meta.get('author', 'Unknown Author')
            if pd.isna(author):
                author = 'Unknown Author'

            s_score = semantic_pool.get(pid, {}).get('norm_semantic_score', 0.0)
            c_score = collab_pool.get(pid, {}).get('norm_collaborative_score', 0.0)
            
            # Weighted Blend
            base_hybrid_score = (s_score * s_weight) + (c_score * c_weight)
            
            # Semantic Drift Penalty
            # If query is provided and semantic relevance is low, penalize aggressively
            if query and s_score < 0.25:
                # Scaled penalty: results with low semantic overlap are pushed down
                # If s_score is 0, penalty is 0.35. If s_score is 0.25, penalty is 0.
                drift_penalty = 0.35 * (1.0 - (s_score / 0.25))
                base_hybrid_score = max(0.05, base_hybrid_score - drift_penalty)

            # Quality Signal
            quality_score = self._compute_quality_score(meta)
            
            # Final Reranked Score
            final_score = base_hybrid_score * quality_score
            
            # 4. Personalization Boost
            has_personal_match = False
            if preferred_categories:
                final_score, has_personal_match = self._apply_preference_boost(final_score, categories, preferred_categories)

            # 5. Confidence Calibration (Believability Layer)
            calibrated_score = self._calibrate_score(final_score)
            
            # Category Normalization
            display_categories = self._normalize_categories(categories)
            
            result = PodcastResult(
                podcast_id=pid,
                title=meta['title'],
                author=author,
                categories=display_categories,
                semantic_score=s_score,
                collaborative_score=c_score,
                blended_score=calibrated_score
            )
            
            # 6. Explanation Phase
            result.explanation = self._generate_explanation(result, meta, has_personal_match)
            blended_results.append(result)

        # 7. Diversity Reranking
        blended_results = self._apply_diversity_penalty(blended_results)

        # 8. Final Ranking & Deduplication
        # Sort by blended score descending
        blended_results.sort(key=lambda x: x.blended_score, reverse=True)
        
        # Remove target podcast if present
        if podcast_id:
            blended_results = [r for r in blended_results if r.podcast_id != podcast_id]
            
        return blended_results[:limit]

    def _apply_preference_boost(self, score: float, categories: str, preferred: List[str]) -> (float, bool):
        """Applies a soft boost if podcast categories match user preferences."""
        if not preferred:
            return score, False
            
        cat_list = [c.strip().lower() for c in str(categories).split(',')]
        pref_list = [p.strip().lower() for p in preferred]
        
        match = any(p in cat_list for p in pref_list)
        if match:
            # Stronger boost: +25% to the base score (capped at 1.0)
            return min(1.0, score * 1.25), True
            
        return score, False

    def _normalize_categories(self, raw_cats: str) -> str:
        """Transforms noisy raw categories into clean display labels."""
        if not raw_cats or pd.isna(raw_cats):
            return "General"
            
        mapping = {
            'news-tech-news': 'Technology News',
            'society-culture': 'Society & Culture',
            'education-how-to': 'Education',
            'business-investing': 'Investing',
            'science-medicine': 'Medicine',
            'arts-design': 'Design',
            'tv-film': 'TV & Film'
        }
        
        parts = [p.strip() for p in raw_cats.split(',')]
        normalized = []
        for p in parts:
            clean = mapping.get(p.lower(), p.replace('-', ' ').title())
            if clean not in normalized:
                normalized.append(clean)
                
        return ", ".join(normalized[:2]) # Keep top 2 for UI

    def _apply_diversity_penalty(self, results: List[PodcastResult]) -> List[PodcastResult]:
        """
        Enhanced diversity penalty to avoid identical top results.
        If a category or author is already present, subsequent items are penalized.
        """
        seen_cats = {}
        seen_authors = {}
        
        # Sort by score descending to apply penalties in order
        for res in sorted(results, key=lambda x: x.blended_score, reverse=True):
            primary_cat = res.categories.split(',')[0].strip()
            author = res.author or "Unknown"
            
            cat_count = seen_cats.get(primary_cat, 0)
            author_count = seen_authors.get(author, 0)
            
            penalty = 0.0
            if cat_count > 0:
                # Increasing penalty for category redundancy
                penalty += 0.05 * cat_count
            if author_count > 0 and author != "Unknown":
                # Increasing penalty for author redundancy
                penalty += 0.04 * author_count
                
            if penalty > 0:
                res.blended_score = max(0.4, res.blended_score - penalty)
            
            seen_cats[primary_cat] = cat_count + 1
            seen_authors[author] = author_count + 1
            
        return results

    def _compute_quality_score(self, meta: Dict) -> float:
        """
        Post-retrieval quality scoring.
        Penalizes weak metadata and boosts rich content.
        Output range: 0.2 - 1.2
        """
        score = 1.0
        title = str(meta.get('title', '')).lower().strip()
        desc = str(meta.get('description', '')).lower().strip()
        author = str(meta.get('author', '')).lower().strip()
        cats = str(meta.get('categories', '')).lower()
        
        if pd.isna(cats): cats = ''

        # 1. Title & URL Penalties
        bad_patterns = ['podcast', 'untitled', 'show', 'test', 'episode', 'my podcast']
        if any(p == title for p in bad_patterns):
            score -= 0.35
        
        if len(title) < 5:
            score -= 0.2

        # Detect URL-like titles (common in low-quality/spam imports)
        if '.com' in title or '.net' in title or 'http' in title:
            score -= 0.4

        # 2. Description Penalties (Aggressive for very short)
        if not desc or desc == 'nan' or len(desc) < 25:
            score -= 0.45  # Massive penalty for almost no description
        elif len(desc) < 60:
            score -= 0.25
        elif len(desc) < 120:
            score -= 0.1
            
        # 3. Filler Detection
        filler_starts = ['welcome to', 'please enjoy', 'hello', 'this is my', 'this is a podcast', 'welcome back']
        if any(desc.startswith(p) for p in filler_starts):
            score -= 0.15
        
        # 4. Institutional/Trusted Author Boost
        trusted_patterns = ['university', 'iheart', 'npr', 'bbc', 'ted', 'microsoft', 'google', 'harvard', 'mit', 'stanford', 'institute', 'wsj', 'nytimes']
        if any(p in author for p in trusted_patterns):
            score += 0.12
        
        # 5. Semantic Drift / Low Quality Category Detection
        # (Heuristic: certain categories are high noise for search)
        if 'kids' in cats or 'family' in cats:
            score -= 0.2
        if 'general' in cats and len(cats.split(',')) == 1:
            score -= 0.1 # Penalize generic categorizations

        # 6. Metadata Boosts (Rewarding high effort)
        if len(desc) > 500:
            score += 0.1
        if len(desc) > 1000:
            score += 0.05
        
        if cats and ',' in cats:
            score += 0.05

        return max(0.2, min(1.2, score))

    def _calibrate_score(self, score: float) -> float:
        """
        Compresses scores into a realistic 78-94% confidence range for top results.
        Prevents clusters and fake 100% scores.
        """
        # Base (0.78) + Range (0.16) * normalized score
        # Using a slight power function to reward very high base scores
        calibrated = 0.78 + (0.16 * (score ** 1.1))
        return round(calibrated, 4)

    def _normalize(self, pool: Dict, score_key: str) -> Dict:
        if not pool: return pool
        
        scores = [c[score_key] for c in pool.values()]
        min_s, max_s = min(scores), max(scores)
        
        diff = max_s - min_s
        for pid in pool:
            raw = pool[pid][score_key]
            pool[pid][f'norm_{score_key}'] = (raw - min_s) / diff if diff > 0 else 1.0
            
        return pool

    def _generate_explanation(self, result: PodcastResult, meta: Dict, has_personal_match: bool = False) -> str:
        """Enhanced rule-based intelligent templating for explanations."""
        primary_cat = result.categories.split(',')[0].strip()
        title = result.title.lower()
        
        # Personalization Boost Explanation
        if has_personal_match:
            return f"Matches your personal interest in {primary_cat}."

        # High Confidence Hybrid
        if result.semantic_score > 0.8 and result.collaborative_score > 0.6:
            return f"A top-tier match: perfectly aligns with your interests in {primary_cat} and is trending among similar users."

        # Semantic/Content Explanation
        if result.semantic_score > result.collaborative_score:
            if any(kw in primary_cat.lower() for kw in ["technology", "science", "innovation"]):
                return f"Focuses on technical deep-dives and innovation within {primary_cat}."
            if any(kw in primary_cat.lower() for kw in ["business", "investing", "startup"]):
                return f"Provides strategic insights into the {primary_cat} and entrepreneurial landscape."
            if any(kw in primary_cat.lower() for kw in ["history", "society", "culture"]):
                return f"Explores the cultural and historical narratives of {primary_cat}."
            
            return f"Highly relevant content focusing on themes related to {primary_cat}."
            
        # Behavioral/Collaborative Explanation
        if result.collaborative_score > 0.7:
            return "Highly recommended by the community for listeners with similar taste profiles."
        
        if result.collaborative_score > 0.4:
            return "Listeners who enjoy similar shows also frequently listen to this podcast."
            
        # Default fallback
        return f"A curated discovery in the {primary_cat} space."
