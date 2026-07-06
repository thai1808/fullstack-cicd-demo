import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app
from models import db

def make_client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_health():
    client = make_client()
    res = client.get("/api/health")
    assert res.status_code == 200

def test_create_and_list_note():
    client = make_client()
    res = client.post("/api/notes", json={"content": "Học Jenkins"})
    assert res.status_code == 201
    res = client.get("/api/notes")
    assert res.status_code == 200
    assert any(n["content"] == "Học Jenkins" for n in res.get_json())
