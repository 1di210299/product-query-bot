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
    description="RAG-based chatbot for product queries with multi-agent architecture",
    version="1.0.0"
)

# Initialize multi-agent systems (only once)
multi_agent_system = None
langgraph_system = None

@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup"""
    global multi_agent_system, langgraph_system
    try:
        print("Initializing multi-agent system...")
        multi_agent_system = MultiAgentSystem()
        print("Multi-agent system ready")
        
        # Initialize LangGraph system if available
        try:
            from src.agents.langgraph_system import LangGraphMultiAgentSystem
            langgraph_system = LangGraphMultiAgentSystem()
            print("LangGraph system ready")
        except ImportError as e:
            print(f"LangGraph system not available: {e}")
            langgraph_system = None
        
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
    return {"message": "Product Query Bot API is running!", "endpoints": ["/query", "/query-langgraph", "/health", "/system/info"]}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "product-query-bot"}

@app.get("/system/info")
async def system_info():
    """Multi-agent system information"""
    info = {}
    if multi_agent_system:
        info["primary_system"] = multi_agent_system.get_system_info()
    if langgraph_system:
        info["langgraph_system"] = langgraph_system.get_system_info()
    return info if info else {"error": "No systems initialized"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process user queries using multi-agent RAG pipeline (original implementation)
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

@app.post("/query-langgraph", response_model=QueryResponse)
async def process_query_langgraph(request: QueryRequest):
    """
    Process user queries using LangGraph-based multi-agent RAG pipeline
    """
    try:
        if not langgraph_system:
            raise HTTPException(status_code=500, detail="LangGraph system not available")
        
        # Process query using the LangGraph system
        result = langgraph_system.process_query(request.query, request.user_id)
        
        if result["status"] == "error":
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
        raise HTTPException(status_code=500, detail=f"Error processing LangGraph query: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
