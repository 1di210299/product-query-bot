# src/rag/generator.py
from openai import OpenAI
from typing import List, Dict
from src.utils.config import Config

class ResponseGenerator:
    def __init__(self):
        self.config = Config()
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        
    def generate_response(self, query: str, retrieved_docs: List[Dict]) -> str:
        """
        Generates response using OpenAI based on retrieved documents
        """
        try:
            # Build context from documents
            context = self._build_context(retrieved_docs)
            
            # Create prompt
            prompt = self._create_prompt(query, context)
            
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert assistant in health and beauty products. Respond helpfully and accurately based only on the information provided."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            generated_response = response.choices[0].message.content.strip()
            print(f"Response generated for: '{query}'")
            return generated_response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Sorry, I couldn't process your query at this time. Error: {str(e)}"
    
    def _build_context(self, retrieved_docs: List[Dict]) -> str:
        """Builds context from retrieved documents"""
        if not retrieved_docs:
            return "No relevant documents found."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(f"Document {i}:\n{doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Creates the prompt for OpenAI"""
        prompt = f"""
Available product information:
{context}

User question: {query}

Instructions:
- Answer based ONLY on the information provided
- If information is not available, say you don't have that specific information
- Be specific about products, prices and ingredients when available
- Maintain a friendly and professional tone
- Include prices if available
- If recommending a product, explain why it's suitable

Response:"""
        
        return prompt