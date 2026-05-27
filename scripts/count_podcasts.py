import json
count = 0
with open('data/raw/podcasts.json', 'r', encoding='utf-8') as f:
    for line in f:
        count += 1
print(f"Total podcasts in raw file: {count:,}")
