"""
Tests for the DELETE /activities/{activity_name}/participants endpoint.
"""

import pytest


def test_unregister_success(client, reset_activities):
    """Test successful unregistration from an activity"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client, reset_activities):
    """Test that unregister actually removes the participant"""
    email = "michael@mergington.edu"
    
    # Verify participant is there
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    initial_count = len(activities["Chess Club"]["participants"])
    
    # Unregister
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": email}
    )
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == initial_count - 1


def test_unregister_activity_not_found(client, reset_activities):
    """Test unregister from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent Club/participants",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_student_not_found(client, reset_activities):
    """Test unregister for student not in activity returns 404"""
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "notamember@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not signed up" in data["detail"]


def test_unregister_then_signup_again(client, reset_activities):
    """Test that student can signup after unregistering"""
    email = "flexible@mergington.edu"
    
    # Sign up
    response1 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Unregister
    response2 = client.delete(
        "/activities/Basketball Team/participants",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Sign up again
    response3 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    assert response3.status_code == 200
    
    # Verify final state
    activities = client.get("/activities").json()
    assert email in activities["Basketball Team"]["participants"]


def test_unregister_multiple_students(client, reset_activities):
    """Test that unregistering one student doesn't affect others"""
    # Chess Club has ["michael@mergington.edu", "daniel@mergington.edu"]
    michael = "michael@mergington.edu"
    daniel = "daniel@mergington.edu"
    
    # Unregister Michael
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": michael}
    )
    
    # Verify Michael is gone but Daniel remains
    activities = client.get("/activities").json()
    assert michael not in activities["Chess Club"]["participants"]
    assert daniel in activities["Chess Club"]["participants"]
