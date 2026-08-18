"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_get_activities_contains_all_activities(client):
    """Test that all expected activities are returned"""
    response = client.get("/activities")
    data = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Track and Field",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    ]
    
    for activity_name in expected_activities:
        assert activity_name in data


def test_activity_has_required_fields(client):
    """Test that each activity has required fields"""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity in data.items():
        assert isinstance(activity, dict), f"{activity_name} should be a dict"
        for field in required_fields:
            assert field in activity, f"{activity_name} missing '{field}' field"


def test_activity_participants_is_list(client):
    """Test that participants in each activity is a list"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        assert isinstance(activity["participants"], list), \
            f"{activity_name} participants should be a list"


def test_activity_max_participants_is_positive_int(client):
    """Test that max_participants is a positive integer"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        assert isinstance(activity["max_participants"], int), \
            f"{activity_name} max_participants should be an int"
        assert activity["max_participants"] > 0, \
            f"{activity_name} max_participants should be positive"
