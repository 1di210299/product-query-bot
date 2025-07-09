# tests/test_api.py
import pytest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.api.main import app

# Create client with correct syntax for older version
client = TestClient(app)  # Without keyword argument

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Product Query Bot API is running!"}

def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "product-query-bot"

def test_query_endpoint_valid_request():
    """Test query endpoint with valid request"""
    test_request = {
        "user_id": "test_user_123",
        "query": "What products do you have available?"
    }
    
    response = client.post("/query", json=test_request)
    assert response.status_code == 200
    
    data = response.json()
    assert data["user_id"] == "test_user_123"
    assert data["query"] == test_request["query"]
    assert "response" in data
    assert "retrieved_docs" in data
    assert "agent_info" in data

def test_query_endpoint_shampoo():
    """Specific test for shampoo query"""
    test_request = {
        "user_id": "test_shampoo",
        "query": "dandruff shampoo"
    }
    
    response = client.post("/query", json=test_request)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["retrieved_docs"]) > 0
