import json
from collections import Counter

# Get matching IDs
subset_ids = set()
with open('data/raw/podcasts.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            subset_ids.add(json.loads(line)['podcast_id'])
        except:
            continue

print("Counting matching reviews...")
match_counts = Counter()
total_matches = 0
with open('data/raw/reviews.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            pid = json.loads(line)['podcast_id']
            if pid in subset_ids:
                match_counts[pid] += 1
                total_matches += 1
        except:
            continue

print(f"Total matching reviews: {total_matches}")
print(f"Top matches: {match_counts.most_common(5)}")
