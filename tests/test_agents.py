# tests/test_agents.py
import pytest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_agent_imports():
    """Test that agent modules can be imported"""
    try:
        from src.agents.multi_agent_system import MultiAgentSystem
        from src.agents.retriever_agent import RetrieverAgent
        from src.agents.responder_agent import ResponderAgent
        
        # Check they are classes
        assert callable(MultiAgentSystem)
        assert callable(RetrieverAgent)
        assert callable(ResponderAgent)
        
        print("Agent import test passed")
    except ImportError as e:
        pytest.fail(f"Agent import failed: {e}")

def test_agent_structure():
    """Test basic agent structure without full initialization"""
    try:
        from src.agents.multi_agent_system import MultiAgentSystem
        
        # Test that the class has expected methods
        assert hasattr(MultiAgentSystem, 'process_query')
        assert hasattr(MultiAgentSystem, 'get_system_info')
        
        print("Agent structure test passed")
    except Exception as e:
        pytest.fail(f"Agent structure test failed: {e}")

def test_basic_config():
    """Test basic configuration for agents"""
    try:
        from src.utils.config import Config
        config = Config()
        
        # Test that required config exists
        assert hasattr(config, 'TOP_K_DOCUMENTS')
        assert hasattr(config, 'MODEL_NAME')
        assert hasattr(config, 'EMBEDDING_MODEL')
        
        print("Agent config test passed")
    except Exception as e:
        pytest.fail(f"Agent config test failed: {e}")

if __name__ == "__main__":
    test_agent_imports()
    test_agent_structure()
    test_basic_config()
    print("All agent tests passed!")
