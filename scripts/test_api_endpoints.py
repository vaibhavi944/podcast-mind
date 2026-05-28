import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing /health...")
    r = requests.get(f"{BASE_URL}/health")
    print(r.status_code, r.json())

def test_recommend():
    print("\nTesting /recommend...")
    params = {
        "query": "history and civilization",
        "podcast_id": "ff269332200b78cbabfe05ce6d2ab038",
        "limit": 3
    }
    r = requests.get(f"{BASE_URL}/recommend", params=params)
    print(r.status_code)
    if r.status_code == 200:
        results = r.json()['results']
        for res in results:
            print(f"- {res['title']} (Blended Score: {res['blended_score']:.4f})")

def test_similar():
    print("\nTesting /similar...")
    params = {"podcast_id": "ff269332200b78cbabfe05ce6d2ab038", "limit": 3}
    r = requests.get(f"{BASE_URL}/similar", params=params)
    print(r.status_code)
    if r.status_code == 200:
        results = r.json()['results']
        for res in results:
            print(f"- {res['title']} (Blended Score: {res['blended_score']:.4f})")

def test_search():
    print("\nTesting /search...")
    params = {"query": "true crime and investigation", "limit": 3}
    r = requests.get(f"{BASE_URL}/search", params=params)
    print(r.status_code)
    if r.status_code == 200:
        results = r.json()['results']
        for res in results:
            print(f"- {res['title']} (Blended Score: {res['blended_score']:.4f})")

if __name__ == "__main__":
    test_health()
    test_recommend()
    test_similar()
    test_search()
