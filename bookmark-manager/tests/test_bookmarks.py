from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_bookmark():
    payload = {
        "url": "https://example.com",
        "title": "Example",
        "description": "An example bookmark",
        "tags": ["reference", "example"],
    }
    response = client.post("/bookmarks", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Example"
    assert set(body["tags"]) == {"reference", "example"}

    bookmark_id = body["id"]
    response = client.get(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
