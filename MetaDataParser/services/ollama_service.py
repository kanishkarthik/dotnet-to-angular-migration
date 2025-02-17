import json
import re
import os
import hashlib
import shutil
import concurrent.futures
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.storage import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import PersistentClient
from config.constants import ASPNETMVC_APP_CONFIG_PATH, ASPNETMVC_APP_PATH, GROQ_API_KEY, CHROMA_DB_PATH
from .base_llm_service import BaseLLMService
from utils.logger import logger

# Load API keys
load_dotenv()
api_key = GROQ_API_KEY

class OllamaService(BaseLLMService):
    def __init__(self, llm_model: str, clear_index: bool = False):
        logger.info("Initializing Ollama Service")
        super().__init__()
        
        logger.info(f"Setting up LLM with model: {llm_model}")
        self.llm = Ollama(model=llm_model, base_url="http://localhost:11434/", temperature=0.1)
        
        logger.info("Configuring embedding model")
        self.embed_model = OllamaEmbedding(model_name=llm_model, base_url="http://localhost:11434")

        logger.info("Setting up global settings")
        self._setup_settings()

        if clear_index:
            self.clear_index()

        self.index = self._load_or_create_index()
        logger.info("OllamaService initialization completed")

    def clear_index(self):
        """Clears existing index for a fresh start"""
        logger.info("Clearing existing index...")
        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)
            logger.info("Index cleared.")
        else:
            logger.info("No existing index to clear.")

    def _setup_settings(self):
        """Configures LLM and embedding settings"""
        Settings.llm = self.llm
        Settings.num_output = 250
        Settings.embed_model = self.embed_model

    def _calculate_documents_hash(self):
        """Calculate a hash of all C# files for change detection"""
        logger.info("Calculating document hash for change detection")
        hash_str = ""
        file_count = 0
        for root, _, files in os.walk(ASPNETMVC_APP_CONFIG_PATH):
            for file in sorted(files):
                if file.endswith('.cs'):
                    file_count += 1
                    with open(os.path.join(root, file), 'rb') as f:
                        hash_str += hashlib.md5(f.read()).hexdigest()
        logger.info(f"Document hash calculation completed for {file_count} files")
        return hashlib.md5(hash_str.encode()).hexdigest()

    def _get_embedding_dimension(self):
        """Get embedding vector size dynamically"""
        logger.info("Determining embedding dimension")
        try:
            dimension = len(self.embed_model.get_text_embedding("test"))
            logger.info(f"Embedding dimension determined: {dimension}")
            return dimension
        except Exception as e:
            logger.error(f"Failed to get embedding dimension: {e}")
            raise

    def _load_existing_index(self, collection):
        """Load existing index if metadata matches"""
        logger.info("Attempting to load existing index")
        try:
            current_dimension = self._get_embedding_dimension()
            logger.info("Checking metadata for embedding dimension")
            metadata = collection.get(where={"type": "embedding_info"})
            if not metadata or not metadata['metadatas']:
                logger.warning("No metadata found for existing index")
                return None

            stored_dimension = metadata['metadatas'][0].get('dimension')
            logger.info(f"Stored dimension: {stored_dimension}, Current dimension: {current_dimension}")
            if stored_dimension != current_dimension:
                logger.warning("Embedding dimension mismatch, re-indexing required.")
                return None

            logger.info("Creating vector store and storage context")
            vector_store = ChromaVectorStore(chroma_collection=collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            logger.info("Successfully loaded existing index")
            return VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, embed_model=self.embed_model)
        except Exception as e:
            logger.warning(f"Failed to load existing index: {e}")
            return None

    def _load_or_create_index(self):
        """Load or create vector index efficiently"""
        logger.info("Initializing index loading process")
        chroma_client = PersistentClient(path=CHROMA_DB_PATH)
        collection_name = "dotnetapp"
        current_dimension = self._get_embedding_dimension()

        if collection_name in chroma_client.list_collections():
            logger.info("Found existing collection, checking hash")
            collection = chroma_client.get_collection(collection_name)
            current_hash = self._calculate_documents_hash()

            try:
                stored_hash = collection.get(where={"type": "document_hash"})
                if stored_hash and stored_hash['documents'][0] == current_hash:
                    logger.info("Document hash matches, attempting to load existing index")
                    existing_index = self._load_existing_index(collection)
                    if existing_index:
                        return existing_index
            except Exception as e:
                logger.error(f"Error checking stored hash: {e}")

        logger.info("Creating new index")
        if collection_name in chroma_client.list_collections():
            logger.info("Deleting existing collection")
            chroma_client.delete_collection(collection_name)
        collection = chroma_client.create_collection(name=collection_name)

        logger.info("Storing metadata and document hash")
        current_hash = self._calculate_documents_hash()
        collection.add(documents=[current_hash], metadatas=[{"type": "document_hash"}], ids=["document_hash"])
        collection.add(documents=["embedding_info"], metadatas=[{"type": "embedding_info", "dimension": current_dimension}], ids=["embedding_info"])

        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        logger.info("Loading documents from directory")
        documents = SimpleDirectoryReader(ASPNETMVC_APP_PATH, required_exts=[".cs"], recursive=True).load_data()
        logger.info(f"Loaded {len(documents)} C# files")

        logger.info("Generating embeddings in parallel")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            embeddings = list(executor.map(self.embed_model.get_text_embedding, [doc.text for doc in documents]))

        logger.info("Adding documents and embeddings to collection")
        collection.add(documents=[doc.text for doc in documents], embeddings=embeddings, ids=[str(i) for i in range(len(documents))])

        logger.info("Creating final index")
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=self.embed_model)

        logger.info(f"New index created successfully with dimension {current_dimension}")
        return index

    def analyze(self, prompt: str) -> str:
        """Perform analysis using the vector index"""
        logger.info(f"Starting analysis with prompt: {prompt}")
        try:
            logger.info("Creating query engine")
            query_engine = self.index.as_query_engine(response_mode="tree_summarize", streaming=True)
            logger.info("Executing query")
            response = query_engine.query(prompt)
            logger.info("Analysis completed successfully")
            return str(response)
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise RuntimeError(f"Analysis error: {e}")
