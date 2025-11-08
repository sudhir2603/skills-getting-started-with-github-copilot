import pytest
from fastapi import status

def test_get_activities(client, sample_activity_data):
    response = client.get("/activities")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Debate Team" in data

def test_signup_activity_success(client):
    email = "new.student@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == status.HTTP_200_OK
    
    # Verify the student was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_signup_activity_full(client):
    # First, fill up the activity
    activity = "Debate Team"
    base_email = "student{}@mergington.edu"
    
    # Add maximum number of participants
    for i in range(15):  # max_participants is 15 for Debate Team
        client.post(f"/activities/{activity}/signup", params={"email": base_email.format(i)})
    
    # Try to add one more
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": "extra.student@mergington.edu"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Activity is full" in response.json()["detail"]

def test_signup_activity_duplicate(client):
    email = "duplicate.student@mergington.edu"
    activity = "Chess Club"
    
    # First signup
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Try to signup again
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in response.json()["detail"].lower()

def test_unregister_activity_success(client):
    # First, sign up a student
    email = "unregister.test@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Now unregister them
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == status.HTTP_200_OK
    
    # Verify they were removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_unregister_activity_not_found(client):
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()

def test_get_nonexistent_activity(client):
    activity = "Nonexistent Club"
    response = client.get(f"/activities/{activity}")
    assert response.status_code == status.HTTP_404_NOT_FOUND