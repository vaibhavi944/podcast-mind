import json

print("Extracting 5 unique IDs from reviews...")
unique_ids = set()
with open('data/raw/reviews.json', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            unique_ids.add(json.loads(line)['podcast_id'])
            if len(unique_ids) >= 5:
                break
        except:
            continue

print(f"Target IDs: {unique_ids}")

found_count = 0
with open('data/raw/podcasts.json', 'r', encoding='utf-8') as f:
    for line in f:
        for target in unique_ids:
            if target in line:
                print(f"Found match for {target}")
                found_count += 1
                break
        if found_count >= len(unique_ids):
            break

print(f"Total matches found: {found_count}")
