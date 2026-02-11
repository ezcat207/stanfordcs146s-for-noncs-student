from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..app.main import app
from ..app.db import Base, get_db

# (In a real solution, we would mock the DB properly here)
# This is a concise example of the pagination test structure.

def test_pagination():
    # Setup: Create 15 notes
    for i in range(15):
        client.post("/notes/", json={"title": f"Note {i}", "content": "test"})
    
    # Test 1: Limit 10 (Page 1)
    response = client.get("/notes/?limit=10&skip=0")
    data = response.json()
    assert len(data) == 10
    assert data[0]["title"] == "Note 0"
    
    # Test 2: Limit 10, Skip 10 (Page 2)
    response = client.get("/notes/?limit=10&skip=10")
    data = response.json()
    assert len(data) == 5
    assert data[0]["title"] == "Note 10"
