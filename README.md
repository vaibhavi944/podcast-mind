# PodcastMind: Hybrid AI Podcast Recommendation System

PodcastMind is a production-style recommendation system designed to deliver highly relevant podcast suggestions with near-zero onboarding friction.

## Core Features
- **Semantic Search:** Natural language search for podcasts based on themes and concepts.
- **Hybrid Recommendations:** Combining content-based filtering (embeddings) with collaborative filtering (ALS).
- **Instant Personalization:** No login required—pick 3 podcasts and get instant results.
- **AI-Powered Explanations:** Real reasoning behind every recommendation using Llama 3.

## Architecture
The system is divided into two main layers:
- **Offline Layer:** Heavy ML computations, metadata normalization, and artifact generation (FAISS indices, ALS models).
- **Online Layer:** A high-performance FastAPI backend for real-time inference and retrieval.

## Project Structure
```text
podcast-mind/
├── data/               # Raw and processed datasets
├── artifacts/          # Serialized models and indices
├── notebooks/          # EDA and experimental pipelines
├── backend/            # FastAPI source code
│   ├── engines/        # Recommendation logic
│   ├── routers/        # API endpoints
│   └── services/       # External integrations (e.g., Groq)
├── frontend/           # React + Vite application
└── tests/              # Unit and integration tests
```

## Getting Started
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables in `.env`.
5. Run the backend: `uvicorn backend.main:app --reload`
