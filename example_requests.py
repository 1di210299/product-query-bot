# example_requests.py
"""
Example scripts to test the Product Query Bot API
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"

def print_response(response, query_text):
    """Prints response in formatted way"""
    print(f"\n{'='*50}")
    print(f"QUERY: {query_text}")
    print(f"{'='*50}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"BOT RESPONSE:")
        print(f"{data['response']}")
        print(f"\nDOCUMENTS FOUND: {len(data['retrieved_docs'])}")
        for i, doc in enumerate(data['retrieved_docs'], 1):
            print(f"  {i}. {doc['metadata']['filename']} (similarity: {doc['distance']:.3f})")
        
        print(f"\nAGENT INFO:")
        agent_info = data['agent_info']
        print(f"  • Retriever: {agent_info['retriever']['docs_found']} docs found")
        print(f"  • Responder: {agent_info['responder']['docs_used']} docs used")
    else:
        print(f"ERROR {response.status_code}: {response.text}")

def test_queries():
    """Test product queries"""
    
    # Example queries
    queries = [
        "What shampoo do you recommend for dandruff?",
        "Do you have any sunscreen available?",
        "What vitamins help with the immune system?",
        "Do you have products for dry skin?",
        "What is the cheapest product you have?",
        "What products contain aloe vera?",
        "I need something to clean my hands",
        "What products do you recommend for facial care?"
    ]
    
    print(f"\nRunning {len(queries)} example queries...")
    
    for i, query in enumerate(queries, 1):
        request_data = {
            "user_id": f"test_user_{i}",
            "query": query
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json=request_data,
                timeout=30
            )
            print_response(response, query)
            
            # Pause between queries
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")

def main():
    """Main function"""
    print("PRODUCT QUERY BOT - API TESTS")
    print("="*60)
    
    # Connectivity test
    print("1. Checking connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("Server connected")
        else:
            print(f"Server responds with error: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"Cannot connect to server: {e}")
        print("Make sure the server is running on http://localhost:8000")
        return
    
    # Run tests
    test_queries()
    
    print(f"\n{'='*60}")
    print("Tests completed!")

if __name__ == "__main__":
    main()
