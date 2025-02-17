import json
import re
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import PromptTemplate, Settings
from llama_index.core.embeddings import resolve_embed_model
from llama_index.embeddings.ollama import OllamaEmbedding
import os
from llama_index.core.storage import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import PersistentClient
import hashlib

from config.constants import ASPNETMVC_APP_CONFIG_PATH, ASPNETMVC_APP_PATH, GROQ_API_KEY, CHROMA_DB_PATH
from .base_llm_service import BaseLLMService
from utils.logger import logger

load_dotenv()
api_key = GROQ_API_KEY 


class OllamaEmbeddingWrapper:
    def __init__(self, embed_model):
        self.embed_model = embed_model

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        # Convert to the format expected by OllamaEmbedding
        nodes = [{"text": text} for text in input]
        return self.embed_model.get_text_embedding_batch(nodes)


class OllamaService(BaseLLMService):
    def __init__(self, llm_model: str, clear_index: bool = False):
        logger.info("Initializing Ollama Service")
        super().__init__()
        self.llm = Ollama(
            model=llm_model,
            base_url="http://localhost:11434/",
            temperature=0.1
        )
        self.embed_model = OllamaEmbedding(
            model_name=llm_model,
            base_url="http://localhost:11434",
            ollama_additional_kwargs={"mirostat": 0}
        )
        
        self._setup_settings()
        
        if clear_index:
            self.clear_index()
            
        self.index = self._load_or_create_index()

    def clear_index(self):
        """Clear the existing index storage"""
        logger.info("Attempting to clear existing index")
        try:
            if os.path.exists(CHROMA_DB_PATH):
                import shutil
                shutil.rmtree(CHROMA_DB_PATH)
                logger.info("Successfully cleared existing index")
            else:
                logger.info("No existing index found to clear")
        except Exception as e:
            logger.error(f"Error clearing index: {str(e)}")
            raise RuntimeError(f"Failed to clear index: {e}")

    def _setup_settings(self):
        logger.info("Setting up Ollama Ingest settings")
        Settings.llm = self.llm
        Settings.num_output = 250
        Settings.embed_model = self.embed_model

    def _calculate_documents_hash(self):
        """Calculate a hash of all documents to detect changes"""
        hash_str = ""
        for root, _, files in os.walk(ASPNETMVC_APP_CONFIG_PATH):
            for file in sorted(files):
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        hash_str += hashlib.md5(f.read()).hexdigest()
        return hashlib.md5(hash_str.encode()).hexdigest()

    def _get_embedding_dimension(self):
        """Get the embedding dimension of the current model"""
        try:
            # Get dimension by embedding a test string
            test_embedding = self.embed_model.get_text_embedding("test")
            return len(test_embedding)
        except Exception as e:
            logger.error(f"Error getting embedding dimension: {str(e)}")
            raise

    def _load_existing_index(self, collection):
        """Attempt to load existing index"""
        try:
            # Get current model's embedding dimension
            current_dimension = self._get_embedding_dimension()
            
            # Check stored dimension
            metadata = collection.get(where={"type": "embedding_info"})
            if not metadata or not metadata['metadatas']:
                logger.info("No embedding dimension info found")
                return None
                
            stored_dimension = metadata['metadatas'][0].get('dimension')
            if stored_dimension != current_dimension:
                logger.info(f"Embedding dimension mismatch: stored={stored_dimension}, current={current_dimension}")
                return None

            vector_store = ChromaVectorStore(chroma_collection=collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex.from_vector_store(
                vector_store,
                storage_context=storage_context,
                embed_model=self.embed_model
            )
            return index
        except Exception as e:
            logger.info(f"Could not load existing index: {str(e)}")
            return None

    def _load_or_create_index(self):
        logger.info("Checking for existing index")
        try:
            chroma_client = PersistentClient(path=CHROMA_DB_PATH)
            collection_name = "dotnetapp"
            
            # Get current embedding dimension
            current_dimension = self._get_embedding_dimension()
            
            # Check if collection exists
            if collection_name in chroma_client.list_collections():
                collection = chroma_client.get_collection(collection_name)
                current_hash = self._calculate_documents_hash()
                
                try:
                    stored_hash = collection.get(where={"type": "document_hash"})
                    if stored_hash and stored_hash['documents'][0] == current_hash:
                        logger.info("Documents unchanged, attempting to load existing index")
                        existing_index = self._load_existing_index(collection)
                        if existing_index:
                            logger.info("Successfully loaded existing index")
                            return existing_index
                except Exception as e:
                    logger.info(f"Error checking document hash: {str(e)}")

            # If we reach here, we need to create a new index
            logger.info("Creating new index")
            if collection_name in chroma_client.list_collections():
                chroma_client.delete_collection(collection_name)
            collection = chroma_client.create_collection(name=collection_name)
            
            # Store the hash and embedding dimension
            current_hash = self._calculate_documents_hash()
            collection.add(
                documents=[current_hash],
                metadatas=[{"type": "document_hash"}],
                ids=["document_hash"]
            )
            collection.add(
                documents=["embedding_info"],
                metadatas=[{"type": "embedding_info", "dimension": current_dimension}],
                ids=["embedding_info"]
            )

            # Create new index
            vector_store = ChromaVectorStore(chroma_collection=collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            documents = SimpleDirectoryReader(
                ASPNETMVC_APP_PATH,
                required_exts=[".cs"],
                recursive=True
            ).load_data()
            
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                embed_model=self.embed_model
            )
            
            logger.info(f"New index created successfully with dimension {current_dimension}")
            return index

        except Exception as e:
            logger.error(f"Error in index loading/creation: {str(e)}")
            raise

    def analyze(self, prompt: str) -> str:
        logger.info(f"Starting analysis with prompt: {prompt}")
        try:
            query_engine = self.index.as_query_engine(
                response_mode="tree_summarize",
                streaming=True
            )
            
            response = query_engine.query(prompt)
            logger.info("Successfully received response from query engine")
            
            return str(response)
        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            raise RuntimeError(f"Error in analysis process: {e}")


