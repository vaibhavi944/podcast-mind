import json

targets = {'bf5bf76d5b6ffbf9a31bba4480383b7f', '18318ad3d298e2bd492866c5bdd8273f', '614cacdd2d628f870a86fae1d99dac04', '8488e8694e66dd616480e12bf427e1de', 'bc5ddad3898e0973eb541577d1df8004'}

print(f"Searching for top reviewed IDs in podcasts.json...")
found = []
with open('data/raw/podcasts.json', 'r', encoding='utf-8') as f:
    for line in f:
        for t in targets:
            if t in line:
                found.append(t)
                print(f"Found {t}!")
if not found:
    print("None of the top 5 reviewed podcasts were found in podcasts.json.")
