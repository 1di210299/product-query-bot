# src/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
    
    # RAG Configuration
    TOP_K_DOCUMENTS = int(os.getenv("TOP_K_DOCUMENTS", 3))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Paths
    DOCS_PATH = "docs/products"
    CHROMA_PERSIST_DIR = "chroma_db"
    
    # Validation
    @classmethod
    def validate(cls):
        errors = []
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not set")
        
        if not os.path.exists(cls.DOCS_PATH):
            errors.append(f"Documents path {cls.DOCS_PATH} does not exist")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True