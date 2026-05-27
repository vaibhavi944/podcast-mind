import json
from collections import Counter

print("Analyzing ID lengths in reviews.json...")
lens = Counter()
with open('data/raw/reviews.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            lens[len(json.loads(line)['podcast_id'])] += 1
        except:
            continue
print(lens)
