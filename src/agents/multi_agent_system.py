# src/agents/multi_agent_system.py
from typing import Dict
from src.agents.retriever_agent import RetrieverAgent
from src.agents.responder_agent import ResponderAgent
from src.rag.retriever import DocumentRetriever

class MultiAgentSystem:
    """
    Multi-agent system coordinator for RAG
    """
    def __init__(self):
        # Create shared retriever instance
        self.shared_retriever = DocumentRetriever()
        
        # Pass shared retriever to agents
        self.retriever_agent = RetrieverAgent(shared_retriever=self.shared_retriever)
        self.responder_agent = ResponderAgent()
        self.system_name = "MultiAgentRAGSystem"
    
    def process_query(self, query: str, top_k: int = 3) -> Dict:
        """
        Processes a query using the multi-agent pipeline
        """
        print(f"{self.system_name}: Starting processing of '{query}'")
        
        try:
            # STEP 1: Retriever Agent searches for documents
            retrieval_result = self.retriever_agent.run(query, top_k)
            
            if retrieval_result["status"] == "error":
                return {
                    "system": self.system_name,
                    "query": query,
                    "final_response": "Error in document search",
                    "retrieved_docs": [],
                    "status": "error",
                    "error": retrieval_result.get("error", "Unknown error")
                }
            
            # STEP 2: Responder Agent generates response
            response_result = self.responder_agent.run(
                query, 
                retrieval_result["retrieved_docs"]
            )
            
            # STEP 3: Combine results
            final_result = {
                "system": self.system_name,
                "query": query,
                "final_response": response_result["response"],
                "retrieved_docs": retrieval_result["retrieved_docs"],
                "status": response_result["status"],
                "agent_results": {
                    "retriever": {
                        "docs_found": retrieval_result["doc_count"],
                        "status": retrieval_result["status"]
                    },
                    "responder": {
                        "docs_used": response_result["docs_used"],
                        "status": response_result["status"]
                    }
                }
            }
            
            print(f"{self.system_name}: Processing completed")
            return final_result
            
        except Exception as e:
            print(f"{self.system_name}: System error - {e}")
            return {
                "system": self.system_name,
                "query": query,
                "final_response": f"System error: {str(e)}",
                "retrieved_docs": [],
                "status": "system_error",
                "error": str(e)
            }
    
    def get_system_info(self) -> Dict:
        """Information about the complete system"""
        return {
            "system_name": self.system_name,
            "description": "Multi-agent RAG system with search and generation",
            "agents": {
                "retriever": self.retriever_agent.get_info(),
                "responder": self.responder_agent.get_info()
            }
        }