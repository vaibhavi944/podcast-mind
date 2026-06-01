# PodcastMind — Demo Script (2-3 Minutes)

This script is designed for a recorded video or a live portfolio presentation.

---

### 1. Introduction (0:00 - 0:30)
*   **Visual:** Opening slide with PodcastMind logo.
*   **Audio:** "Hi, I'm [Name], and this is PodcastMind—a hybrid recommendation system designed to solve the discovery problem in podcasting. Most search engines rely on keywords; PodcastMind relies on semantic meaning and behavioral patterns."

### 2. The Problem & Dataset (0:30 - 0:50)
*   **Visual:** Show a snippet of the raw JSON metadata vs. the cleaned CSV.
*   **Audio:** "We started with a massive 2-million record dataset. The challenge? It was noisy and inconsistent. I engineered a memory-safe preprocessing pipeline that pruned 90% of the noise, leaving us with 20,000 high-quality semantic seeds."

### 3. User Onboarding (0:50 - 1:10)
*   **Visual:** Screen recording of the **TasteOnboarding** overlay.
*   **Audio:** "To respect privacy while delivering immediate value, we use a zero-login onboarding flow. Users simply pick their interests, which are stored in local storage and used to provide a persistent boost to our ranking algorithm."

### 4. Discover & Hybrid Intelligence (1:10 - 1:40)
*   **Visual:** Screen recording of the **Discover** page. Hover over a recommendation explanation.
*   **Audio:** "This is the Discover page. Behind the scenes, our Hybrid Engine is blending content-based signals from FAISS with collaborative signals from an ALS model. Notice the explanation field—it tells the user *why* they're seeing a show, building immediate trust."

### 5. Semantic Search (1:40 - 2:00)
*   **Visual:** Typing "Artificial Intelligence and the future of work" into the **Search** bar.
*   **Audio:** "Traditional search would look for these exact words. Our semantic search understands the *concept*. Even shows that don't have 'Artificial Intelligence' in the title are surfaced because they occupy the same vector space."

### 6. Architecture & Tech Stack (2:00 - 2:30)
*   **Visual:** Show the `architecture_diagram.md` (Mermaid diagram).
*   **Audio:** "Technically, this is a FastAPI backend orchestration with a React frontend. We use SentenceTransformers for embeddings and FAISS for sub-millisecond retrieval. It's a 'retrieval-first' architecture that focuses on deterministic quality rather than black-box LLM generation."

### 7. Conclusion (2:30 - 2:45)
*   **Visual:** Final slide with GitHub link and contact info.
*   **Audio:** "PodcastMind demonstrates how to build professional, explainable recommendation systems that put the user’s interests first. Check out the code on GitHub. Thanks for watching!"
