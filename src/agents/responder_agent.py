# src/agents/responder_agent.py
from typing import List, Dict
from src.rag.generator import ResponseGenerator

class ResponderAgent:
    """
    Agent specialized in generating responses based on documents
    """
    def __init__(self):
        self.generator = ResponseGenerator()
        self.agent_name = "ResponderAgent"
    
    def run(self, query: str, retrieved_docs: List[Dict]) -> Dict:
        """
        Executes response generation
        """
        print(f"{self.agent_name}: Generating response for '{query}'")
        
        try:
            # Generate response using documents
            response = self.generator.generate_response(query, retrieved_docs)
            
            # Prepare result
            result = {
                "agent": self.agent_name,
                "query": query,
                "response": response,
                "status": "success",
                "docs_used": len(retrieved_docs)
            }
            
            print(f"{self.agent_name}: Response generated successfully")
            return result
            
        except Exception as e:
            print(f"{self.agent_name}: Error - {e}")
            return {
                "agent": self.agent_name,
                "query": query,
                "response": f"Sorry, I couldn't generate a response. Error: {str(e)}",
                "status": "error",
                "error": str(e),
                "docs_used": 0
            }
    
    def get_info(self) -> Dict:
        """Agent information"""
        return {
            "agent_name": self.agent_name,
            "description": "Generates responses using OpenAI based on retrieved documents",
            "model": self.generator.config.MODEL_NAME
        }