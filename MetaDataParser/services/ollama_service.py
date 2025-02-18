import json
import re
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import PromptTemplate, Settings
from llama_index.core.embeddings import resolve_embed_model
import os
from pathlib import Path
from llama_index.core.storage import StorageContext
from llama_index.core import load_index_from_storage

from config.constants import ASPNETMVC_APP_PATH, GROQ_API_KEY, GROQ_LARGE_LANGUAGE_MODEL, ROOT_PATH, SAMPLE_METADATA_PATH, INDEX_STORAGE_PATH_2
from .base_llm_service import BaseLLMService
from utils.logger import logger

load_dotenv()
api_key = GROQ_API_KEY

class OllamaService(BaseLLMService):
    def __init__(self, llm_model: str, clear_index: bool = False):
        logger.info("Initializing GroqIngestService")
        super().__init__()
        self.llm = Groq(model=llm_model, api_key=GROQ_API_KEY)
        self.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
        self._setup_settings()
        
        if clear_index:
            logger.info("Clearing existing index based on the reindex request")
            self.clear_index()
            
        self.index = self._load_or_create_index()

    def clear_index(self):
        """Clear the existing index storage"""
        logger.info("Attempting to clear existing index")
        try:
            if os.path.exists(INDEX_STORAGE_PATH_2):
                import shutil
                shutil.rmtree(INDEX_STORAGE_PATH_2)
                logger.info("Successfully cleared existing index")
            else:
                logger.info("No existing index found to clear")
        except Exception as e:
            logger.error(f"Error clearing index: {str(e)}")
            raise RuntimeError(f"Failed to clear index: {e}")

    def _setup_settings(self):
        logger.info("Setting up Groq Ingest settings")
        Settings.llm = self.llm
        Settings.num_output = 250
        Settings.embed_model = self.embed_model

    def _load_or_create_index(self):
        logger.info("Checking for existing index")
        try:
            if os.path.exists(INDEX_STORAGE_PATH_2):
                logger.info("Loading existing index")
                storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_PATH_2)
                return load_index_from_storage(storage_context)
            
            logger.info("No existing index found, creating new one")
            documents = SimpleDirectoryReader(
                ASPNETMVC_APP_PATH,
                required_exts=[".cs"],
                recursive=True
            ).load_data()
            
            index = VectorStoreIndex.from_documents(documents)
            logger.info("Persisting index for future use")
            index.storage_context.persist(persist_dir=INDEX_STORAGE_PATH_2)
            return index
        except Exception as e:
            logger.error(f"Error in index loading/creation: {str(e)}")
            raise

    def analyze(self, query: str = None) -> str:
        try:
            query_engine = self.index.as_query_engine()
            
            template = (
                "Context Information:\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Task: {query_str}\n")
            
            query_engine.update_prompts(PromptTemplate(template=template))

            response = query_engine.query(query)
            logger.info("Successfully received response from query engine")
            logger.info(f"Raw response from query engine: {response}")
            return response.response
        except Exception as e:
            logger.error(f"Error in Groq Ingest analysis: {str(e)}")
            raise RuntimeError(f"Error in Groq Ingest process: {e}")


