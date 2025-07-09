#!/usr/bin/env python3
"""
Demo script to test BOTH Product Query Bot systems
Compares Original vs LangGraph implementations
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
QUERIES = [
    {
        "user_id": "demo_user_1",
        "query": "What shampoo do you recommend for dandruff?"
    },
    {
        "user_id": "demo_user_2",
        "query": "Do you have sunscreen available?"
    },
    {
        "user_id": "demo_user_3",
        "query": "What vitamins help with the immune system?"
    },
    {
        "user_id": "demo_user_4",
        "query": "Do you have products for dry skin?"
    }
]

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("Health check: OK")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Cannot connect to server. Is it running?")
        print("Try: python -m src.api.main")
        return False

def test_system_info():
    """Test system info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/system/info")
        if response.status_code == 200:
            data = response.json()
            print("System info: OK")
            if "primary_system" in data:
                print("  Original system: Available")
            if "langgraph_system" in data:
                print("  LangGraph system: Available")
            return True
        else:
            print(f"System info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"System info error: {e}")
        return False

def test_query(query_payload, endpoint="query", system_name="Original"):
    """Test a single query on specified endpoint"""
    try:
        print(f"\nQuery ({system_name}): {query_payload['query']}")
        print("-" * 60)

        response = requests.post(
            f"{BASE_URL}/{endpoint}",
            json=query_payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"Status: Success")
            
            response_text = data.get('response', '')
            if len(response_text) > 150:
                print(f"Response: {response_text[:150]}...")
            else:
                print(f"Response: {response_text}")
            
            docs_count = len(data.get('retrieved_docs', []))
            print(f"Documents retrieved: {docs_count}")

            if 'agent_info' in data:
                info = data['agent_info']
                retriever_docs = info.get('retriever', {}).get('docs_found', 0)
                responder_docs = info.get('responder', {}).get('docs_used', 0)
                print(f"Retriever: {retriever_docs} docs found")
                print(f"Responder: {responder_docs} docs used")

            return True, docs_count > 0
        else:
            print(f"Query failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False, False

    except Exception as e:
        print(f"Error during query: {e}")
        return False, False

def compare_systems(query_payload):
    """Compare both systems with the same query"""
    print(f"\nCOMPARING SYSTEMS")
    print("=" * 70)
    
    # Test Original System
    success_orig, docs_orig = test_query(query_payload, "query", "Original")
    
    print("\n" + "─" * 70)
    
    # Test LangGraph System  
    success_lang, docs_lang = test_query(query_payload, "query-langgraph", "LangGraph")
    
    # Comparison summary
    print(f"\nCOMPARISON SUMMARY:")
    print(f"   Original: {'Working' if success_orig and docs_orig else 'Issues'}")
    print(f"   LangGraph: {'Working' if success_lang and docs_lang else 'Issues'}")
    
    return success_orig and docs_orig, success_lang and docs_lang

def main():
    """Main function for the demo"""
    print("PRODUCT QUERY BOT - DUAL SYSTEM DEMO")
    print("=" * 70)
    print("Testing both Original and LangGraph multi-agent implementations")
    print()

    if not test_health():
        return
    
    if not test_system_info():
        return

    print(f"\nRUNNING {len(QUERIES)} TEST QUERIES:")
    print("=" * 70)

    orig_successes = 0
    lang_successes = 0
    
    for index, query in enumerate(QUERIES, start=1):
        print(f"\nTEST {index}/{len(QUERIES)}")
        
        orig_success, lang_success = compare_systems(query)
        
        if orig_success:
            orig_successes += 1
        if lang_success:
            lang_successes += 1

        if index < len(QUERIES):
            time.sleep(1)

    # Final Summary
    print("\n" + "=" * 70)
    print(f"FINAL RESULTS:")
    print(f"   Original System: {orig_successes}/{len(QUERIES)} queries successful")
    print(f"   LangGraph System: {lang_successes}/{len(QUERIES)} queries successful")
    
    if lang_successes == len(QUERIES):
        print("LangGraph system working perfectly!")
    if orig_successes == len(QUERIES):
        print("Original system working perfectly!")
    elif orig_successes == 0:
        print("Original system needs debugging")
    
    print(f"\nNext steps:")
    print(f"   • API docs: {BASE_URL}/docs")
    print(f"   • System info: {BASE_URL}/system/info")
    print(f"   • Use /query-langgraph for reliable results")

if __name__ == "__main__":
    main()
