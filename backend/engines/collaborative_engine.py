from typing import Dict
from backend.utils.loader import artifacts
from backend.config import settings

class CollaborativeEngine:
    """
    Handles behavioral similarity using pre-trained ALS model.
    """
    
    def __init__(self):
        self.model = artifacts.als_model
        self.mappings = artifacts.collab_mappings
        self.metadata = artifacts.metadata

    def get_candidates(self, podcast_id: str, top_k: int = settings.TOP_K_CANDIDATES) -> Dict[str, Dict]:
        """
        Retrieves top-N behaviorally similar podcasts based on co-interest patterns.
        """
        if not self.model or not self.mappings:
            return {}

        if podcast_id not in self.mappings['id_to_idx']:
            return {}

        # 1. Map ID to matrix index
        p_idx = self.mappings['id_to_idx'][podcast_id]
        
        # 2. Query ALS model for similar items
        # implicit similar_items returns (ids, scores)
        ids, scores = self.model.similar_items(p_idx, N=top_k + 1)
        
        # 3. Map back to IDs and Metadata
        candidates = {}
        for i in range(1, len(ids)):  # Skip self (index 0)
            idx = ids[i]
            score = scores[i]
            pod_id = self.mappings['idx_to_id'][idx]
            
            # Use metadata from the metadata mapping
            pod_meta = self.metadata[idx]
            
            candidates[pod_id] = {
                'collaborative_score': float(score),
                'metadata': pod_meta
            }
            
        return candidates
