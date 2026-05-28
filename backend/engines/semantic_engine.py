import faiss
import numpy as np
from typing import List, Dict
from backend.utils.loader import artifacts
from backend.config import settings

class SemanticEngine:
    """
    Handles vector-based similarity search using FAISS.
    """
    
    def __init__(self):
        self.index = artifacts.faiss_index
        self.metadata = artifacts.metadata
        self.model = artifacts.embedding_model

    def get_candidates(self, query: str, top_k: int = settings.TOP_K_CANDIDATES) -> Dict[str, Dict]:
        """
        Retrieves top-N semantically similar podcasts for a given text query.
        """
        if not self.model or not self.index:
            return {}

        # 1. Encode query to vector
        query_vector = self.model.encode([query], normalize_embeddings=True)
        
        # 2. Search FAISS index
        distances, indices = self.index.search(query_vector, top_k)
        
        # 3. Map back to metadata
        candidates = {}
        for i in range(len(indices[0])):
            idx = indices[0][i]
            score = distances[0][i]
            
            # Map index to podcast_id (metadata_mapping is expected to be a list or dict of dicts)
            pod_meta = self.metadata[idx]
            pod_id = pod_meta['podcast_id']
            
            candidates[pod_id] = {
                'semantic_score': float(score),
                'metadata': pod_meta
            }
            
        return candidates

    def get_similar_by_id(self, podcast_id: str, top_k: int = 20) -> Dict[str, Dict]:
        """
        (Placeholder) If we had stored embeddings for all IDs, we could retrieve 
        similar shows directly by index. For now, we rely on text queries or 
        collaborative filtering for ID-based retrieval.
        """
        # In this implementation, we mostly use text queries for semantic search.
        return {}
