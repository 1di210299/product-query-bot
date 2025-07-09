# src/rag/retriever.py
import os
import glob
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from src.utils.config import Config

class DocumentRetriever:
    def __init__(self):
        self.config = Config()
        self.embedding_model = SentenceTransformer(self.config.EMBEDDING_MODEL)
        self.client = chromadb.Client()
        self.collection = None
        self._setup_collection()
        self._load_documents()
    
    def _setup_collection(self):
        """Sets up the ChromaDB collection"""
        try:
            # Delete collection if it exists (for testing)
            try:
                self.client.delete_collection("products")
            except:
                pass
            
            # Create new collection
            self.collection = self.client.create_collection(
                name="products",
                metadata={"description": "Product documents for RAG"}
            )
            print("ChromaDB collection created")
        except Exception as e:
            print(f"Error creating collection: {e}")
            raise
    
    def _load_documents(self):
        """Loads documents from the docs/products folder"""
        try:
            docs_pattern = os.path.join(self.config.DOCS_PATH, "*.txt")
            doc_files = glob.glob(docs_pattern)
            
            if not doc_files:
                raise FileNotFoundError(f"No documents found in {self.config.DOCS_PATH}")
            
            documents = []
            metadatas = []
            ids = []
            
            for doc_file in doc_files:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                doc_id = os.path.basename(doc_file).replace('.txt', '')
                
                documents.append(content)
                metadatas.append({
                    "filename": os.path.basename(doc_file),
                    "source": doc_file,
                    "doc_id": doc_id
                })
                ids.append(doc_id)
            
            # Add to ChromaDB
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Loaded {len(documents)} documents into ChromaDB")
            return len(documents)
            
        except Exception as e:
            print(f"Error loading documents: {e}")
            raise
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Searches for documents similar to the query
        """
        if top_k is None:
            top_k = self.config.TOP_K_DOCUMENTS
        
        try:
            # Perform search
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # Format results
            retrieved_docs = []
            
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    doc = {
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if results['distances'] else None,
                        "id": results['ids'][0][i]
                    }
                    retrieved_docs.append(doc)
            
            print(f"Found {len(retrieved_docs)} documents for: '{query}'")
            return retrieved_docs
            
        except Exception as e:
            print(f"Error in search: {e}")
            return []
    
    def get_collection_info(self):
        """Information about the collection"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": "products",
                "embedding_model": self.config.EMBEDDING_MODEL
            }
        except Exception as e:
            print(f"Error getting info: {e}")
            return {}