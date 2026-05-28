from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Artifacts & Data Paths
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Specific Artifact Files
FAISS_INDEX_PATH = ARTIFACTS_DIR / "faiss_index.index"
METADATA_PATH = ARTIFACTS_DIR / "podcast_metadata.pkl"
ALS_MODEL_PATH = ARTIFACTS_DIR / "als_model.pkl"
COLLAB_MAPPINGS_PATH = ARTIFACTS_DIR / "collaborative_mappings.pkl"
HYBRID_CONFIG_PATH = ARTIFACTS_DIR / "hybrid_config.pkl"
PODCASTS_CSV_PATH = PROCESSED_DATA_DIR / "podcasts_subset_20k.csv"

# Model Settings
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Recommendation Defaults
DEFAULT_SEMANTIC_WEIGHT = 0.7
DEFAULT_COLLABORATIVE_WEIGHT = 0.3
TOP_K_CANDIDATES = 50
DEFAULT_REC_LIMIT = 5

# App Settings
APP_NAME = "PodcastMind API"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
