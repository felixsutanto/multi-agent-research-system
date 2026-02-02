"""Tests for the FastAPI endpoints"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client"""
    from src.api.main import app
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_returns_200(self, client):
        """Test health endpoint returns 200"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_health_has_timestamp(self, client):
        """Test health response includes timestamp"""
        response = client.get("/health")
        data = response.json()
        
        assert "timestamp" in data
        assert "version" in data


class TestRootEndpoint:
    """Tests for root endpoint"""
    
    def test_root_returns_api_info(self, client):
        """Test root endpoint returns API info"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "name" in data
        assert "endpoints" in data


class TestResearchEndpoint:
    """Tests for research endpoint"""
    
    def test_research_validates_query_length(self, client):
        """Test that short queries are rejected"""
        response = client.post(
            "/research",
            json={"query": "short"}  # Less than 10 chars
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_research_accepts_valid_query(self, client):
        """Test that valid queries are accepted (may timeout without API keys)"""
        # This test just checks the endpoint accepts the request format
        # Actual research requires API keys
        response = client.post(
            "/research",
            json={
                "query": "What are the benefits of exercise?",
                "include_evaluation": False
            }
        )
        
        # Should either succeed or fail with API key error, not validation error
        assert response.status_code != 422
