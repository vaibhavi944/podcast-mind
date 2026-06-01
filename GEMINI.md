# PodcastMind Project Instructions

## Architectural Core
PodcastMind is a **retrieval-first and ranking-first** recommendation system. Its intelligence is derived from semantic search (FAISS + Embeddings), collaborative filtering (ALS), and sophisticated hybrid reranking.

## Critical Directives
- **NO LLM/Groq Integration:** Do not integrate LLMs or Groq for the current phase. This is an intentional decision to prioritize recommendation quality, latency, and determinism over natural language generation.
- **Priority Focus:**
  1. Recommendation relevance & ranking quality.
  2. Quality reranking layer (metadata penalization/boosting).
  3. Confidence calibration (realistic scores).
  4. User cold-start via lightweight onboarding (No login).
  5. Session-based personalization (Local storage).
- **Engineering Values:** Fast, deterministic, explainable, and cost-efficient architecture.

## Tech Stack
- **Backend:** FastAPI, FAISS, Implicit (ALS), SentenceTransformers.
- **Frontend:** React + Vite, TailwindCSS (for styling), Lucide-React.
- **Personalization:** Browser-local storage (localStorage), no centralized user database.
