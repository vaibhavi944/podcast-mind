import json
target = '943d1c4349913bde09ef82b69f83cfdf'
found = False
with open('data/raw/podcasts.json', 'r', encoding='utf-8') as f:
    for line in f:
        if target in line:
            print(f"Found record: {line.strip()}")
            found = True
            break
if not found:
    print("Not found")
