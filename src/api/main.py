# src/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import os
from src.agents.multi_agent_system import MultiAgentSystem

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Product Query Bot",
    description="RAG-based chatbot for product queries",
    version="1.0.0"
)

# Initialize multi-agent system (only once)
multi_agent_system = None

@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup"""
    global multi_agent_system
    try:
        print("Initializing multi-agent system...")
        multi_agent_system = MultiAgentSystem()
        print("Multi-agent system ready")
    except Exception as e:
        print(f"Error initializing system: {e}")
        raise

# Pydantic models for validation
class QueryRequest(BaseModel):
    user_id: str
    query: str

class QueryResponse(BaseModel):
    user_id: str
    query: str
    response: str
    retrieved_docs: list = []
    agent_info: dict = {}

@app.get("/")
async def root():
    return {"message": "Product Query Bot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "product-query-bot"}

@app.get("/system/info")
async def system_info():
    """Multi-agent system information"""
    if multi_agent_system:
        return multi_agent_system.get_system_info()
    return {"error": "System not initialized"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process user queries using multi-agent RAG pipeline
    """
    try:
        if not multi_agent_system:
            raise HTTPException(status_code=500, detail="Multi-agent system not initialized")
        
        # Process query using the multi-agent system
        result = multi_agent_system.process_query(request.query)
        
        if result["status"] == "error" or result["status"] == "system_error":
            raise HTTPException(status_code=500, detail=result.get("error", "Error processing query"))
        
        return QueryResponse(
            user_id=request.user_id,
            query=request.query,
            response=result["final_response"],
            retrieved_docs=result["retrieved_docs"],
            agent_info=result.get("agent_results", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",  # FIXED: complete path
        host="0.0.0.0",
        port=8000,
        reload=True
    )
