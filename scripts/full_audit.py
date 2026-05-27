import json
from tqdm import tqdm

print("Extracting IDs from podcasts.json...")
pod_ids = set()
with open('data/raw/podcasts.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            pod_ids.add(json.loads(line)['podcast_id'])
        except:
            continue

print(f"Total unique IDs in podcasts.json: {len(pod_ids):,}")

print("Extracting IDs from reviews.json...")
rev_ids = set()
with open('data/raw/reviews.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            rev_ids.add(json.loads(line)['podcast_id'])
        except:
            continue

print(f"Total unique IDs in reviews.json: {len(rev_ids):,}")

overlap = pod_ids.intersection(rev_ids)
print(f"Overlap size: {len(overlap)}")
print(f"Overlapping IDs: {list(overlap)[:10]}")

if overlap:
    target = list(overlap)[0]
    print(f"\nExample overlapping ID: {target}")
    with open('data/raw/podcasts.json', 'r', encoding='utf-8') as f:
        for line in f:
            if target in line:
                print(f"Podcasts record: {line.strip()}")
                break
    with open('data/raw/reviews.json', 'r', encoding='utf-8') as f:
        for line in f:
            if target in line:
                print(f"Reviews record: {line.strip()}")
                break
