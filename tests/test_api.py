# tests/test_api.py
import pytest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient

def test_basic_import():
    """Test that we can import the main module"""
    try:
        from src.api.main import app
        assert app is not None
        print("Import test passed")
    except Exception as e:
        pytest.fail(f"Import failed: {e}")

def test_basic_endpoints():
    """Test basic endpoints without full initialization"""
    try:
        from src.api.main import app
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("Root endpoint test passed")
        
        # Test health endpoint  
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("Health endpoint test passed")
        
    except Exception as e:
        pytest.fail(f"Basic endpoint test failed: {e}")

def test_config_validation():
    """Test configuration validation"""
    try:
        from src.utils.config import Config
        config = Config()
        
        # Check that config attributes exist
        assert hasattr(config, 'OPENAI_API_KEY')
        assert hasattr(config, 'TOP_K_DOCUMENTS')
        assert hasattr(config, 'MODEL_NAME')
        print("Config validation test passed")
        
    except Exception as e:
        pytest.fail(f"Config test failed: {e}")

if __name__ == "__main__":
    test_basic_import()
    test_basic_endpoints()
    test_config_validation()
    print("All basic tests passed!")
