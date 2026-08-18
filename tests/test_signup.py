"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_success(client, reset_activities):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_adds_participant(client, reset_activities):
    """Test that signup actually adds the participant"""
    email = "newstudent@mergington.edu"
    
    # Get initial participant list
    activities_response = client.get("/activities")
    initial_participants = activities_response.json()["Basketball Team"]["participants"].copy()
    
    # Sign up
    client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    
    # Check that participant was added
    activities_response = client.get("/activities")
    updated_participants = activities_response.json()["Basketball Team"]["participants"]
    
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_activity_not_found(client, reset_activities):
    """Test signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_returns_400(client, reset_activities):
    """Test that duplicate signup returns 400 error"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_different_activities(client, reset_activities):
    """Test that student can sign up for multiple different activities"""
    email = "versatile@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for different activity
    response2 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Basketball Team"]["participants"]


def test_signup_various_activities(client, reset_activities):
    """Test signup works for various activities"""
    email = "tester@mergington.edu"
    activities_to_test = ["Programming Class", "Drama Club", "Debate Club"]
    
    for activity in activities_to_test:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200, f"Failed to sign up for {activity}"
