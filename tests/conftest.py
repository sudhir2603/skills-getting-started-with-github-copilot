import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_activity_data():
    return {
        "Chess Club": {
            "description": "Learn and play chess with fellow students",
            "schedule": "Every Monday and Wednesday after school",
            "max_participants": 20,
            "participants": ["student1@mergington.edu", "student2@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Every Tuesday after school",
            "max_participants": 15,
            "participants": []
        }
    }