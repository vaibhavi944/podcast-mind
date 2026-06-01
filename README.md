# PodcastMind: Hybrid AI Podcast Recommendation System

PodcastMind is a production-grade discovery platform that moves beyond keyword matching. It utilizes semantic vector search and collaborative filtering to deliver highly relevant, explainable podcast suggestions with zero-login friction.

---

## 🚀 The Value Proposition
*   **Semantic Discovery:** Find shows based on *meaning*, not just keywords.
*   **Hybrid Intelligence:** Blends content-based retrieval (FAISS) with behavioral modeling (ALS).
*   **Instant Personalization:** No accounts required. Local-first onboarding provides immediate value.
*   **Trust Through Explanations:** Every recommendation includes a clear, rule-based reason for its ranking.

---

## 🛠️ Architecture & Tech Stack

### High-Level Architecture
```mermaid
graph LR
    Data[2M+ Raw Records] --> Clean[Preprocessing Pipeline]
    Clean --> Embed[MiniLM Embeddings]
    Embed --> Vector[FAISS Index]
    Vector --> Engine[Hybrid Ranking Engine]
    Engine --> API[FastAPI Backend]
    API --> UI[React Frontend]
```

### Technology Stack
*   **Backend:** FastAPI, Python
*   **Machine Learning:** SentenceTransformers, FAISS, Implicit (ALS), Scikit-Learn
*   **Frontend:** React (Vite), TailwindCSS, Lucide-React
*   **Data:** Pandas, NumPy, JSONL Streaming

---

## 🧠 Engineering Highlights

### 1. Semantic Retrieval Engine
We transformed podcast metadata into 384-dimensional dense vectors using the `all-MiniLM-L6-v2` model. Retrieval is handled by `FAISS`, enabling sub-millisecond similarity search across the entire dataset.

### 2. Multi-Stage Hybrid Ranking
Recommendations are not just retrieved; they are ranked. Our pipeline includes:
*   **Weighted Blending:** Balancing semantic relevance with behavioral popularity.
*   **Quality Reranking:** Aggressive heuristics to penalize "spammy" metadata or poor descriptions.
*   **Preference Boosting:** A +25% soft-boost for user-selected categories from onboarding.
*   **Confidence Calibration:** Scores are compressed into a psychologically realistic 78%-94% range.

### 3. Data Integrity & Scaling
Handled a massive 2M+ record dataset through memory-safe JSONL streaming. Implemented strict semantic filtering to prune 90% of the noise, ensuring the engine focuses on content-rich entries.

---

## 🖼️ User Experience

### Onboarding
A lightweight, zero-login "Taste Onboarding" flow allows users to tune their feed in under 10 seconds.

### Intelligent Discovery
The Discover page evolves as the user interacts. Selecting a show triggers the behavioral engine to find "More Like This" gems.

### Explainable AI
Every podcast card surfaces an explanation (e.g., *"Matches your interest in Technology"*), providing transparency and building user trust.

---

## 📈 Evaluation & Results
The system has been evaluated for:
*   **Diversity:** Preventing "category collapse" in top results.
*   **Relevance:** Tested across technical, historical, and ambiguous natural language queries.
*   **Latency:** Average API response time of ~2.0s on CPU-based inference.

---

## 🏁 Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js (for frontend)

### Installation
1.  **Clone the Repo:** `git clone https://github.com/your-username/podcast-mind`
2.  **Backend:**
    ```bash
    python -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    uvicorn backend.main:app --reload
    ```
3.  **Frontend:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## 🗺️ Roadmap & Future Improvements
*   [ ] Live User Feedback Loop (Replacing synthetic ALS data)
*   [ ] Multilingual Embedding Support
*   [ ] Cross-Session Personalization Sync (Optional Auth)
*   [ ] Advanced Learning-to-Rank (LTR) Layer

---
*Developed by [Your Name] as a showcase of modern Recommender System architecture.*
