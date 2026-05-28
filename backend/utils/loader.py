import pickle
import faiss
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from backend.config import settings

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArtifactLoader:
    """
    Handles the safe loading of persisted AI artifacts from disk.
    
    In production engineering, we load pre-computed artifacts rather than 
    re-training models on startup to ensure high availability and 
    predictable performance.
    """
    
    def __init__(self):
        self.metadata: Optional[Dict] = None
        self.faiss_index: Optional[faiss.Index] = None
        self.als_model: Optional[Any] = None
        self.collab_mappings: Optional[Dict] = None
        self.hybrid_config: Optional[Dict] = None
        self.embedding_model: Optional[SentenceTransformer] = None

    def load_all(self):
        """Orchestrates the loading of all required artifacts."""
        logger.info("Initializing artifact loading sequence...")
        
        self.metadata = self._load_pickle(settings.METADATA_PATH, "Metadata Mapping")
        logger.info("[OK] Metadata Mapping loaded")
        
        self.faiss_index = self._load_faiss(settings.FAISS_INDEX_PATH)
        logger.info("[OK] FAISS Index loaded")
        
        self.als_model = self._load_pickle(settings.ALS_MODEL_PATH, "ALS Model")
        logger.info("[OK] ALS Model loaded")
        
        self.collab_mappings = self._load_pickle(settings.COLLAB_MAPPINGS_PATH, "Collaborative Mappings")
        logger.info("[OK] Collaborative Mappings loaded")
        
        self.hybrid_config = self._load_pickle(settings.HYBRID_CONFIG_PATH, "Hybrid Config")
        logger.info("[OK] Hybrid Config loaded")
        
        # Load Embedding Model (SentenceTransformer)
        try:
            logger.info(f"Loading Embedding Model: {settings.EMBEDDING_MODEL_NAME}")
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            logger.info("[OK] Embedding Model loaded")
        except Exception as e:
            logger.error(f"Failed to load Embedding Model: {e}")
            raise

        logger.info("All AI artifacts loaded successfully.")

    def _load_pickle(self, path: Path, label: str) -> Any:
        if not path.exists():
            logger.error(f"Critical Error: {label} not found at {path}")
            raise FileNotFoundError(f"{label} missing.")
        
        with open(path, "rb") as f:
            data = pickle.load(f)
        logger.info(f"{label} loaded successfully.")
        return data

    def _load_faiss(self, path: Path) -> faiss.Index:
        if not path.exists():
            logger.error(f"Critical Error: FAISS Index not found at {path}")
            raise FileNotFoundError("FAISS Index missing.")
        
        index = faiss.read_index(str(path))
        logger.info("FAISS Index loaded successfully.")
        return index

# Singleton instance for global use
artifacts = ArtifactLoader()
