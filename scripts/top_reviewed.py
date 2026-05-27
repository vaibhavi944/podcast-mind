import json
from collections import Counter

print("Counting reviews per podcast...")
counts = Counter()
with open('data/raw/reviews.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            counts[json.loads(line)['podcast_id']] += 1
        except:
            continue

print("\nTop 10 most reviewed podcasts:")
for pid, count in counts.most_common(10):
    print(f"ID: {pid} | Reviews: {count}")
