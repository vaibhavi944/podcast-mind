import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import warnings

# Ensure backend is discoverable
sys.path.append(os.path.abspath("."))

from backend.engines.hybrid_engine import HybridEngine
from backend.utils.loader import artifacts

warnings.filterwarnings('ignore')

def evaluate_query(engine, query, limit=10, preferred_categories=None):
    results = engine.recommend(
        query=query, 
        limit=limit, 
        preferred_categories=preferred_categories
    )
    
    eval_data = []
    for i, res in enumerate(results):
        full_meta = next((m for m in artifacts.metadata if m['podcast_id'] == res.podcast_id), {})
        
        eval_data.append({
            'R': i + 1,
            'Score': f"{res.blended_score*100:.1f}%",
            'Title': res.title[:40],
            'Author': (res.author or "N/A")[:20],
            'Cats': res.categories[:30],
            'Sem': f"{res.semantic_score:.2f}",
            'Col': f"{res.collaborative_score:.2f}",
            'Desc': full_meta.get('description', '')[:50].replace('\n', ' ') + "..."
        })
    
    return pd.DataFrame(eval_data)

def main():
    print("Initializing Hybrid Engine...")
    artifacts.load_all()
    engine = HybridEngine()
    
    tests = [
        ("AI and future society", None),
        ("Modern productivity", ["Technology", "Business"]),
        ("Ancient Rome Archaeology", None),
        ("Business startups", None),
        ("interesting stories", None)
    ]
    
    for query, prefs in tests:
        print(f"\nQUERY: {query} | PREFS: {prefs}")
        df = evaluate_query(engine, query, preferred_categories=prefs)
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
