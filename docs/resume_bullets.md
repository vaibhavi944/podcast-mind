# PodcastMind — Resume Impact Bullets

These bullets are optimized for modern ATS (Applicant Tracking Systems) and technical recruiters, focusing on quantifiable impact, architectural decisions, and specific toolsets.

---

### One-Line Version (For concise experience sections)
*   Engineered a hybrid recommendation system (FastAPI/React) using FAISS vector search and ALS collaborative filtering to deliver personalized, sub-second podcast discovery for 20k+ records.

---

### Two-Line Version (For more detailed experience sections)
*   Architected a "retrieval-first" hybrid recommendation engine combining semantic embeddings (MiniLM) and behavioral modeling (ALS).
*   Implemented a multi-stage ranking pipeline including quality reranking, personalization boosting, and confidence calibration to optimize recommendation relevance and UX trust.

---

### Detailed Version (For project-focused resumes or portfolios)
*   **Hybrid Recommendation Engine:** Built a production-grade discovery system combining semantic retrieval (SentenceTransformers + FAISS) with collaborative filtering (Implicit/ALS).
*   **Multi-Stage Ranking Pipeline:** Developed a custom reranking layer that integrates metadata quality penalties, category-based personalization boosts (+25%), and confidence score calibration (78-94% range).
*   **Data Engineering:** Engineered a memory-safe preprocessing pipeline for 2M+ records, implementing strict semantic filtering and quality heuristics to prune 90% of noisy data.
*   **Personalization & Explanability:** Designed a zero-login "soft onboarding" experience using browser local storage to provide instant personalization and rule-based recommendation explanations.
*   **Tech Stack:** FastAPI (Backend), React + Tailwind (Frontend), FAISS (Vector DB), Scikit-Learn (Normalization), SentenceTransformers (NLP).

---

### Key Technical Keywords
`Recommender Systems`, `Vector Search`, `FAISS`, `Matrix Factorization (ALS)`, `Hybrid Ranking`, `Semantic Retrieval`, `NLP`, `Sentence Embeddings`, `FastAPI`, `React`, `Data Preprocessing`.
