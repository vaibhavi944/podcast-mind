import os
import sys
import pandas as pd
from typing import List, Optional

# Add project root to path
sys.path.append(os.getcwd())

from backend.utils.loader import artifacts
from backend.engines.hybrid_engine import HybridEngine

def run_test(name: str, query: str, prefs: Optional[List[str]] = None):
    print(f"\n=== TEST: {name} ===")
    print(f"Query: '{query}'")
    print(f"Preferences: {prefs}")
    
    engine = HybridEngine()
    results = engine.recommend(query=query, preferred_categories=prefs, limit=5)
    
    for i, res in enumerate(results):
        print(f"{i+1}. {res.title} [{res.categories}]")
        print(f"   Author: {res.author}")
        print(f"   Score: {res.blended_score}")
        print(f"   Explanation: {res.explanation}")
    
    return results

def main():
    print("Loading artifacts...")
    artifacts.load_all()
    
    # Scenario 1: Student interested in AI
    # Onboarding: Tech, Science
    res_ai_pref = run_test("Scenario 1 (AI + Tech Prefs)", "Artificial Intelligence", ["technology", "science"])
    res_ai_no_pref = run_test("Scenario 1 (AI No Prefs)", "Artificial Intelligence", [])

    # Scenario 2: History enthusiast
    # Onboarding: History, Society & Culture
    run_test("Scenario 2 (History Enthusiast)", "World War II", ["history", "society-culture"])

    # Scenario 3: Psychology listener
    # Onboarding: Psychology, Health
    run_test("Scenario 3 (Psychology Listener)", "Human behavior", ["psychology", "health"])

    # Scenario 4: Business/startup listener
    # Onboarding: Business, Investing
    run_test("Scenario 4 (Business Listener)", "Startup growth", ["business", "investing"])

    # Scenario 5: New user with no preferences
    run_test("Scenario 5 (New User)", "Comedy", [])

    # CRITICAL CHECK: Contrast check
    print("\n\n=== CRITICAL CHECK: Contrast Check ===")
    query = "latest trends"
    user_a = run_test("User A (AI + Tech)", query, ["technology"])
    user_b = run_test("User B (History + Philosophy)", query, ["history", "philosophy"])
    
    # Compare top result
    if user_a[0].podcast_id != user_b[0].podcast_id:
        print("\nSUCCESS: Onboarding preferences successfully influenced top rankings!")
    else:
        print("\nWARNING: Onboarding preferences did NOT change top result. Checking if any results differ...")
        ids_a = [r.podcast_id for r in user_a]
        ids_b = [r.podcast_id for r in user_b]
        if ids_a != ids_b:
            print("SUCCESS: Result sets differ, even if top result is same.")
        else:
            print("FAILURE: Result sets are identical. Personalization boost may be too weak or category matching failed.")

if __name__ == "__main__":
    main()
