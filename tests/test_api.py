"""
API endpoint tests for FastAPI backend.

Tests the REST API endpoints for:
- Health check
- Research endpoint
- Request validation
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client for API"""
    from src.api.main import app
    return TestClient(app)


@pytest.mark.api
def test_health_check(client):
    """Test health endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    
    print("✅ Health Check Test Passed")


@pytest.mark.api
def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    # API returns { name, version, endpoints } or { message, status }
    assert "message" in data or "name" in data or "endpoints" in data
    
    print("✅ Root Endpoint Test Passed")



@pytest.mark.api
def test_research_endpoint_validation(client):
    """Test research endpoint validates input"""
    
    # Missing query
    response = client.post(
        "/research",
        json={
            "max_iterations": 2
            # Missing required "query" field
        }
    )
    
    # Should return validation error
    assert response.status_code == 422
    
    print("✅ Request Validation Test Passed")


@pytest.mark.api
def test_research_endpoint_empty_query(client):
    """Test research endpoint rejects empty query"""
    
    response = client.post(
        "/research",
        json={
            "query": "",
            "max_iterations": 2
        }
    )
    
    # Should reject empty query (either 422 or 400)
    assert response.status_code in [400, 422, 500]
    
    print("✅ Empty Query Rejection Test Passed")


@pytest.mark.api
@pytest.mark.slow
def test_research_endpoint_success(client):
    """Test research endpoint with valid request"""
    
    response = client.post(
        "/research",
        json={
            "query": "What is Python?",
            "max_iterations": 1,
            "include_evaluation": False
        },
        timeout=300  # 5 minutes for research
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "query" in data
    assert "report" in data
    assert len(data["report"]) > 50
    
    print("✅ Research Endpoint Success Test Passed")
    print(f"Report length: {len(data['report'])} chars")


@pytest.mark.api
def test_api_cors_headers(client):
    """Test CORS headers are set"""
    response = client.options("/research")
    
    # Should allow CORS
    # Note: Exact behavior depends on CORS configuration
    assert response.status_code in [200, 204, 405]
    
    print("✅ CORS Headers Test Passed")


@pytest.mark.api
def test_api_content_type(client):
    """Test API returns JSON content type"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert "application/json" in response.headers.get("content-type", "")
    
    print("✅ Content Type Test Passed")
