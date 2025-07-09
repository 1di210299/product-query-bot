# tests/test_rag.py
import pytest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.retriever import DocumentRetriever
from src.rag.generator import ResponseGenerator

class TestDocumentRetriever:
    """Tests for DocumentRetriever"""
    
    @pytest.fixture
    def retriever(self):
        """Fixture that creates a retriever for testing"""
        return DocumentRetriever()
    
    def test_collection_setup(self, retriever):
        """Test that collection is configured correctly"""
        assert retriever.collection is not None
        assert retriever.collection.count() > 0
        
    def test_search_basic(self, retriever):
        """Basic search test"""
        results = retriever.search("shampoo", top_k=2)
        
        assert isinstance(results, list)
        assert len(results) <= 2
        assert len(results) > 0
        
        # Verify result structure
        doc = results[0]
        assert "content" in doc
        assert "metadata" in doc
        assert "id" in doc
        assert "distance" in doc
    
    def test_search_caspa(self, retriever):
        """Specific search test for dandruff"""
        results = retriever.search("caspa", top_k=3)
        
        assert len(results) > 0
        # First result should be most relevant (lower distance)
        assert results[0]["distance"] < results[-1]["distance"]
        
        # Should find anti-dandruff shampoo
        content_lower = results[0]["content"].lower()
        assert "shampoo" in content_lower or "caspa" in content_lower
    
    def test_search_empty_query(self, retriever):
        """Test with empty query"""
        results = retriever.search("", top_k=1)
        # Should handle gracefully
        assert isinstance(results, list)
    
    def test_search_top_k_parameter(self, retriever):
        """Test top_k parameter"""
        results_1 = retriever.search("product", top_k=1)
        results_3 = retriever.search("product", top_k=3)
        
        assert len(results_1) <= 1
        assert len(results_3) <= 3
        assert len(results_3) >= len(results_1)
    
    def test_get_collection_info(self, retriever):
        """Test collection information"""
        info = retriever.get_collection_info()
        
        assert isinstance(info, dict)
        assert "total_documents" in info
        assert "collection_name" in info
        assert info["total_documents"] > 0


class TestResponseGenerator:
    """Tests for ResponseGenerator"""
    
    @pytest.fixture
    def generator(self):
        """Fixture that creates a generator for testing"""
        return ResponseGenerator()
    
    @pytest.fixture
    def sample_docs(self):
        """Sample documents for testing"""
        return [
            {
                "content": "Anti-Dandruff Shampoo Premium\nIngredients: Ketoconazole 2%\nPrice: $15.99",
                "metadata": {"filename": "shampoo.txt"},
                "id": "shampoo_anticaspa"
            },
            {
                "content": "Moisturizing Cream\nIngredients: Hyaluronic acid\nPrice: $22.50",
                "metadata": {"filename": "crema.txt"},
                "id": "crema_hidratante"
            }
        ]
    
    def test_build_context(self, generator, sample_docs):
        """Test context building"""
        context = generator._build_context(sample_docs)
        
        assert isinstance(context, str)
        assert "Document 1:" in context
        assert "Document 2:" in context
        assert "Anti-Dandruff Shampoo" in context
        assert "Moisturizing Cream" in context
    
    def test_build_context_empty(self, generator):
        """Test empty context"""
        context = generator._build_context([])
        assert "No relevant documents found" in context
    
    def test_create_prompt(self, generator, sample_docs):
        """Test prompt creation"""
        context = generator._build_context(sample_docs)
        prompt = generator._create_prompt("What shampoo do you recommend?", context)
        
        assert isinstance(prompt, str)
        assert "What shampoo do you recommend?" in prompt
        assert "Anti-Dandruff Shampoo" in prompt
        assert "Instructions:" in prompt
    
    def test_generate_response_structure(self, generator, sample_docs):
        """Test generated response structure"""
        # Only test that it doesn't fail, without making real OpenAI call
        query = "test query"
        
        # Test error handling with empty docs
        response = generator.generate_response(query, [])
        assert isinstance(response, str)
        assert len(response) > 0


def test_config_import():
    """Test that config can be imported"""
    try:
        from src.utils.config import Config
        config = Config()
        assert config.DOCS_PATH == "docs/products"
        assert config.TOP_K_DOCUMENTS >= 1
        print("Config import test passed")
    except Exception as e:
        pytest.fail(f"Config import failed: {e}")

def test_documents_exist():
    """Test that product documents exist"""
    import glob
    
    docs_pattern = "docs/products/*.txt"
    doc_files = glob.glob(docs_pattern)
    
    assert len(doc_files) >= 5, f"Expected at least 5 documents, found {len(doc_files)}"
    
    # Check specific files exist
    expected_files = ["shampoo_anticaspa.txt", "crema_hidratante.txt", "protector_solar.txt"]
    found_files = [os.path.basename(f) for f in doc_files]
    
    for expected in expected_files:
        assert expected in found_files, f"Missing expected file: {expected}"
    
    print(f"Found {len(doc_files)} product documents")

def test_document_content():
    """Test that documents have valid content"""
    import glob
    
    docs_pattern = "docs/products/*.txt"
    doc_files = glob.glob(docs_pattern)
    
    for doc_file in doc_files[:3]:  # Test first 3 files
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        assert len(content) > 50, f"Document {doc_file} seems too short"
        assert "Precio:" in content or "Price:" in content, f"Document {doc_file} missing price info"
    
    print("Document content validation passed")

def test_basic_rag_components():
    """Test basic RAG component imports"""
    try:
        # Test that we can import the classes without initializing
        from src.rag.generator import ResponseGenerator
        from src.rag.retriever import DocumentRetriever
        
        # Check they are classes
        assert callable(ResponseGenerator)
        assert callable(DocumentRetriever)
        
        print("RAG component imports passed")
    except ImportError as e:
        pytest.fail(f"RAG component import failed: {e}")

if __name__ == "__main__":
    test_config_import()
    test_documents_exist()
    test_document_content()
    test_basic_rag_components()
    print("All RAG tests passed!")
