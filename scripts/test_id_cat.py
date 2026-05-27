import json
target = '52e3d2c4fab4e80a8bb75ad144671d96'
found = False
with open('data/raw/categories.json', 'r', encoding='utf-8') as f:
    for line in f:
        if target in line:
            print(f"Found in categories: {line.strip()}")
            found = True
            break
if not found:
    print("Not found")
