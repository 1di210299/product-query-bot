#!/bin/bash
# examples.sh - Script with example commands to test the API

echo "PRODUCT QUERY BOT - USAGE EXAMPLES"
echo "======================================"
echo ""

# API base URL
BASE_URL="http://localhost:8000"

echo "1. Health Check:"
curl -X GET "$BASE_URL/health" | jq '.'
echo ""

echo "2. System Info:"
curl -X GET "$BASE_URL/system/info" | jq '.'
echo ""

echo "3. Query Examples:"
echo ""

echo "Query about anti-dandruff shampoo:"
curl -X POST "$BASE_URL/query" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user123", 
       "query": "What shampoo do you recommend for dandruff?"
     }' | jq '.'
echo ""

echo "Query about sunscreen:"
curl -X POST "$BASE_URL/query" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user456", 
       "query": "Do you have sunscreen available?"
     }' | jq '.'
echo ""

echo "Query about vitamins:"
curl -X POST "$BASE_URL/query" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user789", 
       "query": "What vitamins help with the immune system?"
     }' | jq '.'
echo ""

echo "Query about products for dry skin:"
curl -X POST "$BASE_URL/query" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user101", 
       "query": "Do you have products for dry skin?"
     }' | jq '.'
echo ""

echo "Examples completed!"
echo "Tip: Make sure the server is running with:"
echo "   python -m src.api.main"