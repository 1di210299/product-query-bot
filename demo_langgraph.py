#!/usr/bin/env python3
"""
Demo script specifically for LangGraph system
Tests the working LangGraph implementation
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

QUERIES = [
    {
        "user_id": "langgraph_test_1",
        "query": "What shampoo do you recommend for dandruff?"
    },
    {
        "user_id": "langgraph_test_2", 
        "query": "Do you have sunscreen available?"
    },
    {
        "user_id": "langgraph_test_3",
        "query": "What vitamins help with the immune system?"
    },
    {
        "user_id": "langgraph_test_4",
        "query": "Do you have products for dry skin?"
    },
    {
        "user_id": "langgraph_test_5",
        "query": "What is the cheapest product you have?"
    }
]

def test_langgraph_system():
    """Test the LangGraph system with all queries"""
    print("LANGGRAPH SYSTEM DEMO")
    print("=" * 50)
    print("Testing the working LangGraph multi-agent implementation")
    print()
    
    # Health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("Server is running")
        else:
            print("Server not responding")
            return
    except:
        print("Cannot connect to server")
        print("Run: python -m src.api.main")
        return
    
    success_count = 0
    
    for i, query in enumerate(QUERIES, 1):
        print(f"\nQUERY {i}/{len(QUERIES)}")
        print("=" * 50)
        print(f"Query: {query['query']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{BASE_URL}/query-langgraph",
                json=query,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print("Status: Success")
                print(f"Response: {data['response'][:120]}...")
                print(f"Documents found: {len(data['retrieved_docs'])}")
                
                # Show document titles
                for j, doc in enumerate(data['retrieved_docs'][:2], 1):
                    filename = doc['metadata'].get('filename', 'Unknown')
                    distance = doc.get('distance', 0)
                    print(f"   {j}. {filename} (similarity: {distance:.3f})")
                
                # Agent info
                agent_info = data.get('agent_info', {})
                retriever = agent_info.get('retriever', {})
                responder = agent_info.get('responder', {})
                print(f"Retriever: {retriever.get('docs_found', 0)} docs")
                print(f"Responder: {responder.get('docs_used', 0)} docs")
                
                success_count += 1
                
            else:
                print(f"Failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        if i < len(QUERIES):
            time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"RESULTS: {success_count}/{len(QUERIES)} queries successful")
    
    if success_count == len(QUERIES):
        print("LangGraph system working perfectly!")
        print("Ready for production demo")
    else:
        print("Some queries failed")
    
    print(f"\nFor interactive testing:")
    print(f"   Web UI: {BASE_URL}/docs")
    print(f"   System info: {BASE_URL}/system/info")

if __name__ == "__main__":
    test_langgraph_system()