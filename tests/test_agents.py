# tests/test_agents.py
import pytest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.retriever_agent import RetrieverAgent
from src.agents.responder_agent import ResponderAgent
from src.agents.multi_agent_system import MultiAgentSystem

class TestRetrieverAgent:
    """Tests for RetrieverAgent"""
    
    @pytest.fixture
    def retriever_agent(self):
        """Fixture for RetrieverAgent"""
        return RetrieverAgent()
    
    def test_agent_initialization(self, retriever_agent):
        """Test agent initialization"""
        assert retriever_agent.agent_name == "RetrieverAgent"
        assert retriever_agent.retriever is not None
    
    def test_run_successful_search(self, retriever_agent):
        """Test successful execution"""
        result = retriever_agent.run("shampoo", top_k=2)
        
        assert isinstance(result, dict)
        assert result["agent"] == "RetrieverAgent"
        assert result["query"] == "shampoo"
        assert result["status"] == "success"
        assert "retrieved_docs" in result
        assert "doc_count" in result
        assert result["doc_count"] >= 0
    
    def test_run_with_different_queries(self, retriever_agent):
        """Test with different queries"""
        queries = ["caspa", "sunscreen", "vitamins"]
        
        for query in queries:
            result = retriever_agent.run(query, top_k=1)
            assert result["status"] == "success"
            assert result["query"] == query
            assert len(result["retrieved_docs"]) <= 1
    
    def test_get_info(self, retriever_agent):
        """Test agent information"""
        info = retriever_agent.get_info()
        
        assert isinstance(info, dict)
        assert info["agent_name"] == "RetrieverAgent"
        assert "description" in info
        assert "collection_info" in info


class TestResponderAgent:
    """Tests for ResponderAgent"""
    
    @pytest.fixture
    def responder_agent(self):
        """Fixture for ResponderAgent"""
        return ResponderAgent()
    
    @pytest.fixture
    def sample_retrieved_docs(self):
        """Sample retrieved documents"""
        return [
            {
                "content": "Anti-Dandruff Shampoo Premium\nIngredients: Ketoconazole 2%\nPrice: $15.99",
                "metadata": {"filename": "shampoo.txt"},
                "id": "shampoo_anticaspa"
            }
        ]
    
    def test_agent_initialization(self, responder_agent):
        """Test agent initialization"""
        assert responder_agent.agent_name == "ResponderAgent"
        assert responder_agent.generator is not None
    
    def test_run_with_docs(self, responder_agent, sample_retrieved_docs):
        """Test execution with documents"""
        result = responder_agent.run("What shampoo do you recommend?", sample_retrieved_docs)
        
        assert isinstance(result, dict)
        assert result["agent"] == "ResponderAgent"
        assert result["query"] == "What shampoo do you recommend?"
        assert "response" in result
        assert "status" in result
        assert result["docs_used"] == 1
    
    def test_run_without_docs(self, responder_agent):
        """Test execution without documents"""
        result = responder_agent.run("test query", [])
        
        assert isinstance(result, dict)
        assert result["docs_used"] == 0
        assert isinstance(result["response"], str)
    
    def test_get_info(self, responder_agent):
        """Test agent information"""
        info = responder_agent.get_info()
        
        assert isinstance(info, dict)
        assert info["agent_name"] == "ResponderAgent"
        assert "description" in info
        assert "model" in info


class TestMultiAgentSystem:
    """Tests for MultiAgentSystem"""
    
    @pytest.fixture
    def multi_agent_system(self):
        """Fixture for MultiAgentSystem"""
        return MultiAgentSystem()
    
    def test_system_initialization(self, multi_agent_system):
        """Test system initialization"""
        assert multi_agent_system.system_name == "MultiAgentRAGSystem"
        assert multi_agent_system.retriever_agent is not None
        assert multi_agent_system.responder_agent is not None
    
    def test_process_query_successful(self, multi_agent_system):
        """Test successful query processing"""
        result = multi_agent_system.process_query("What products do you have?", top_k=2)
        
        assert isinstance(result, dict)
        assert result["system"] == "MultiAgentRAGSystem"
        assert result["query"] == "What products do you have?"
        assert "final_response" in result
        assert "retrieved_docs" in result
        assert "status" in result
        assert "agent_results" in result
        
        # Verify agent results
        agent_results = result["agent_results"]
        assert "retriever" in agent_results
        assert "responder" in agent_results
        assert agent_results["retriever"]["status"] == "success"
        assert agent_results["responder"]["status"] == "success"
    
    def test_process_query_different_topics(self, multi_agent_system):
        """Test with different topics"""
        topics = [
            "dandruff shampoo",
            "sunscreen",
            "vitamins",
            "hygiene products"
        ]
        
        for topic in topics:
            result = multi_agent_system.process_query(topic, top_k=1)
            assert result["status"] == "success"
            assert len(result["retrieved_docs"]) >= 0
            assert isinstance(result["final_response"], str)
            assert len(result["final_response"]) > 0
    
    def test_get_system_info(self, multi_agent_system):
        """Test system information"""
        info = multi_agent_system.get_system_info()
        
        assert isinstance(info, dict)
        assert info["system_name"] == "MultiAgentRAGSystem"
        assert "description" in info
        assert "agents" in info
        assert "retriever" in info["agents"]
        assert "responder" in info["agents"]
    
    def test_process_query_empty(self, multi_agent_system):
        """Test with empty query"""
        result = multi_agent_system.process_query("", top_k=1)
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert "final_response" in result
        assert "status" in result
