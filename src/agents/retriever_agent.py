# src/agents/retriever_agent.py
from typing import List, Dict
from src.rag.retriever import DocumentRetriever

class RetrieverAgent:
    """
    Agent specialized in searching for relevant documents
    """
    def __init__(self):
        self.retriever = DocumentRetriever()
        self.agent_name = "RetrieverAgent"
    
    def run(self, query: str, top_k: int = 3) -> Dict:
        """
        Executes document search
        """
        print(f"{self.agent_name}: Searching documents for '{query}'")
        
        try:
            # Search for relevant documents
            retrieved_docs = self.retriever.search(query, top_k)
            
            # Prepare result
            result = {
                "agent": self.agent_name,
                "query": query,
                "retrieved_docs": retrieved_docs,
                "status": "success",
                "doc_count": len(retrieved_docs)
            }
            
            print(f"{self.agent_name}: Found {len(retrieved_docs)} documents")
            return result
            
        except Exception as e:
            print(f"{self.agent_name}: Error - {e}")
            return {
                "agent": self.agent_name,
                "query": query,
                "retrieved_docs": [],
                "status": "error",
                "error": str(e),
                "doc_count": 0
            }
    
    def get_info(self) -> Dict:
        """Agent information"""
        collection_info = self.retriever.get_collection_info()
        return {
            "agent_name": self.agent_name,
            "description": "Searches for relevant documents using semantic embeddings",
            "collection_info": collection_info
        }