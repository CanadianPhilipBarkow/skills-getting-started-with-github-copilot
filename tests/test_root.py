"""
Tests for the root endpoint (GET /).
"""

import pytest


def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    
    # Should return a redirect status
    assert response.status_code == 307
    # Should redirect to the static index.html
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follow(client):
    """Test that following the redirect works"""
    response = client.get("/", follow_redirects=True)
    
    # After redirect, should be successful
    assert response.status_code == 200
