# src/agents/langgraph_system.py
from typing import Dict, TypedDict
from langgraph.graph import StateGraph, END
from src.agents.retriever_agent import RetrieverAgent
from src.agents.responder_agent import ResponderAgent

class AgentState(TypedDict):
    """State shared between agents"""
    query: str
    user_id: str
    retrieved_docs: list
    final_response: str
    retriever_status: str
    responder_status: str

class LangGraphMultiAgentSystem:
    """
    LangGraph-based multi-agent system for RAG pipeline
    Demonstrates framework usage while maintaining existing agent logic
    """
    
    def __init__(self):
        self.retriever_agent = RetrieverAgent()
        self.responder_agent = ResponderAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("retriever", self._retriever_node)
        workflow.add_node("responder", self._responder_node)
        
        # Define the flow
        workflow.set_entry_point("retriever")
        workflow.add_edge("retriever", "responder")
        workflow.add_edge("responder", END)
        
        return workflow.compile()
    
    def _retriever_node(self, state: AgentState) -> AgentState:
        """Retriever agent node"""
        result = self.retriever_agent.run(state["query"])
        
        state["retrieved_docs"] = result["retrieved_docs"]
        state["retriever_status"] = result["status"]
        
        return state
    
    def _responder_node(self, state: AgentState) -> AgentState:
        """Responder agent node"""
        result = self.responder_agent.run(
            state["query"], 
            state["retrieved_docs"]
        )
        
        state["final_response"] = result["response"]
        state["responder_status"] = result["status"]
        
        return state
    
    def process_query(self, query: str, user_id: str = "default") -> Dict:
        """Process query using LangGraph workflow"""
        initial_state = AgentState(
            query=query,
            user_id=user_id,
            retrieved_docs=[],
            final_response="",
            retriever_status="",
            responder_status=""
        )
        
        # Execute the graph
        final_state = self.graph.invoke(initial_state)
        
        return {
            "system": "LangGraphMultiAgentSystem",
            "query": query,
            "user_id": user_id,
            "final_response": final_state["final_response"],
            "retrieved_docs": final_state["retrieved_docs"],
            "status": "success",
            "agent_results": {
                "retriever": {
                    "status": final_state["retriever_status"],
                    "docs_found": len(final_state["retrieved_docs"])
                },
                "responder": {
                    "status": final_state["responder_status"],
                    "docs_used": len(final_state["retrieved_docs"])
                }
            }
        }
    
    def get_system_info(self) -> Dict:
        """System information"""
        return {
            "system_name": "LangGraphMultiAgentSystem",
            "description": "Multi-agent RAG system using LangGraph framework",
            "framework": "LangGraph",
            "agents": {
                "retriever": self.retriever_agent.get_info(),
                "responder": self.responder_agent.get_info()
            },
            "workflow": ["retriever", "responder"]
        }