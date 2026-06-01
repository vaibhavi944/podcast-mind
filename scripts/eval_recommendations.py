import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
from datetime import datetime

# Ensure backend is discoverable
sys.path.append(os.path.abspath("."))

from backend.engines.hybrid_engine import HybridEngine
from backend.utils.loader import artifacts

warnings.filterwarnings('ignore')

class RecommendationEvaluator:
    def __init__(self):
        print("Initializing Evaluator and Hybrid Engine...")
        artifacts.load_all()
        self.engine = HybridEngine()
        self.test_queries = [
            {"query": "Artificial Intelligence and future of society", "tag": "Tech/AI"},
            {"query": "Modern productivity", "prefs": ["Technology", "Business"], "tag": "Personalization"},
            {"query": "Ancient Rome and Archaeology", "tag": "History/Niche"},
            {"query": "Business startups and entrepreneurship", "tag": "Diversity/Business"},
            {"query": "interesting stories", "tag": "Ambiguous/Broad"}
        ]

    def run_suite(self):
        report_lines = [
            "# PodcastMind Recommendation Quality Report",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Executive Summary\n"
        ]
        
        results_summary = []
        
        for test in self.test_queries:
            query = test["query"]
            prefs = test.get("prefs")
            tag = test["tag"]
            
            print(f"Running Eval: {query} ({tag})...")
            
            results = self.engine.recommend(query=query, preferred_categories=prefs, limit=10)
            
            # Metrics
            avg_semantic = np.mean([r.semantic_score for r in results]) if results else 0
            diversity_score = self._calculate_diversity(results)
            top_score = results[0].blended_score if results else 0
            
            results_summary.append({
                "Tag": tag,
                "Query": query,
                "Avg Semantic": f"{avg_semantic:.2f}",
                "Diversity": f"{diversity_score:.2f}",
                "Top Score": f"{top_score*100:.1f}%"
            })
            
            # Detailed Markdown Section
            report_lines.append(f"### TEST: {query} ({tag})")
            if prefs:
                report_lines.append(f"*User Preferences: {prefs}*")
            
            table_header = "| Rank | Score | Title | Author | Categories | Semantic | Explanation |"
            table_sep = "|------|-------|-------|--------|------------|----------|-------------|"
            report_lines.append(table_header)
            report_lines.append(table_sep)
            
            for i, res in enumerate(results):
                clean_title = res.title.replace("|", "\\|")
                report_lines.append(f"| {i+1} | {res.blended_score*100:.1f}% | {clean_title} | {res.author} | {res.categories} | {res.semantic_score:.2f} | {res.explanation} |")
            
            report_lines.append("\n")

        # Add Summary Table to Report
        summary_df = pd.DataFrame(results_summary)
        report_lines.insert(4, summary_df.to_markdown(index=False))
        
        # Save Report
        report_path = Path("artifacts/eval_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        
        print(f"\nEvaluation Complete. Report saved to {report_path}")

    def _calculate_diversity(self, results):
        if not results: return 0
        cats = [r.categories.split(',')[0].strip() for r in results]
        unique_cats = len(set(cats))
        return unique_cats / len(results)

if __name__ == "__main__":
    evaluator = RecommendationEvaluator()
    evaluator.run_suite()
