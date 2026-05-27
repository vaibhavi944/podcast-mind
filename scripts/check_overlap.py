import pandas as pd
import json
from tqdm import tqdm

print("Loading subset...")
subset_df = pd.read_csv('data/processed/podcasts_subset.csv')
subset_pids = set(subset_df['podcast_id'])

print("Scanning reviews for podcast IDs...")
reviews_pids = set()
total_reviews = 0
with open('data/raw/reviews.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            total_reviews += 1
            reviews_pids.add(json.loads(line)['podcast_id'])
        except:
            continue

overlap = subset_pids.intersection(reviews_pids)
print(f"\nAudit Results:")
print(f"Total Usable Podcasts (Semantic Subset): {len(subset_pids):,}")
print(f"Total Unique Podcasts in Reviews:       {len(reviews_pids):,}")
print(f"Overlap:                                {len(overlap):,} ({len(overlap)/len(subset_pids):.2%})")
print(f"Total Reviews scanned:                  {total_reviews:,}")
