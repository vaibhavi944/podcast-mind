import os
import sys
import json
from typing import List, Optional

# Add project root to path
sys.path.append(os.getcwd())

from backend.utils.loader import artifacts
from backend.engines.hybrid_engine import HybridEngine

def generate_evidence():
    print("Loading artifacts...")
    artifacts.load_all()
    engine = HybridEngine()
    
    evidence = {}

    # 1. Search Results Evidence
    queries = ["AI startups", "Ancient Rome", "Psychology"]
    evidence["search_results"] = {}
    for q in queries:
        results = engine.recommend(query=q, limit=3)
        evidence["search_results"][q] = [
            {"title": r.title, "categories": r.categories, "explanation": r.explanation} 
            for r in results
        ]

    # 2. Example JSON: /recommend (with query and prefs)
    recommend_results = engine.recommend(
        query="innovation", 
        preferred_categories=["Technology", "Science"],
        limit=2
    )
    evidence["recommend_json"] = [r.dict() for r in recommend_results]

    # 3. Example JSON: /search
    search_results = engine.recommend(
        query="history of medicine", 
        s_weight=1.0, 
        c_weight=0.0, 
        limit=2
    )
    evidence["search_json"] = [r.dict() for r in search_results]

    # 4. Personalization Contrast (User A vs User B)
    query = "latest trends"
    user_a_results = engine.recommend(query=query, preferred_categories=["Technology"], limit=3)
    user_b_results = engine.recommend(query=query, preferred_categories=["History"], limit=3)
    
    evidence["contrast"] = {
        "User A (Tech)": [{"title": r.title, "score": r.blended_score} for r in user_a_results],
        "User B (History)": [{"title": r.title, "score": r.blended_score} for r in user_b_results]
    }

    # Save to file
    with open("artifacts/deployment_evidence.json", "w") as f:
        json.dump(evidence, f, indent=2)
    print("Evidence generated and saved to artifacts/deployment_evidence.json")

if __name__ == "__main__":
    generate_evidence()
