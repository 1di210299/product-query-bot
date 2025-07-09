# tests/test_langgraph.py
import pytest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_langgraph_import():
    """Test that LangGraph system can be imported"""
    try:
        from src.agents.langgraph_system import LangGraphMultiAgentSystem, AgentState
        
        # Check they are classes/types
        assert callable(LangGraphMultiAgentSystem)
        assert AgentState is not None
        
        print("LangGraph system import test passed")
    except ImportError as e:
        pytest.fail(f"LangGraph system import failed: {e}")

def test_langgraph_structure():
    """Test LangGraph system structure without full initialization"""
    try:
        from src.agents.langgraph_system import LangGraphMultiAgentSystem
        
        # Test that the class has expected methods
        assert hasattr(LangGraphMultiAgentSystem, 'process_query')
        assert hasattr(LangGraphMultiAgentSystem, 'get_system_info')
        assert hasattr(LangGraphMultiAgentSystem, '_build_graph')
        
        print("LangGraph structure test passed")
    except Exception as e:
        pytest.fail(f"LangGraph structure test failed: {e}")

if __name__ == "__main__":
    test_langgraph_import()
    test_langgraph_structure()
    print("All LangGraph tests passed!")