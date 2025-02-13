import json
import re
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import PromptTemplate, Settings
from llama_index.core.embeddings import resolve_embed_model
import os

from config.constants import ASPNETMVC_APP_PATH, GROQ_API_KEY, GROQ_LARGE_LANGUAGE_MODEL, ROOT_PATH, SAMPLE_METADATA_PATH
from .base_llm_service import BaseLLMService
from utils.logger import logger

load_dotenv()
api_key = GROQ_API_KEY 


def get_sample_metadata() -> str:
    wmetadata_structure = ''
        # read json as string config/metadata_sample.json
    with open(SAMPLE_METADATA_PATH, 'r') as file:
        # read json as string config/metadata_sample
        metadata_structure = file.read()
    return metadata_structure

class GroqIngestService(BaseLLMService):
    def __init__(self):
        logger.info("Initializing GroqIngestService")
        super().__init__()
        self.llm = Groq(model=GROQ_LARGE_LANGUAGE_MODEL, api_key=GROQ_API_KEY)
        self.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
        self._setup_settings()

    def _setup_settings(self):
        logger.debug("Setting up Groq Ingest settings")
        Settings.llm = self.llm
        Settings.num_output = 250
        Settings.embed_model = self.embed_model

    def analyze(self, country_code: str, payment_method: str) -> str:
        logger.info(f"Starting Groq Ingest analysis for country: {country_code}, payment method: {payment_method}")
        try:
            metadata_structure = get_sample_metadata()
            base_query = (
                f"Analyze the provided ASP.NET MVC codebase and generate JSON metadata only if "
                f"there are explicit configurations or implementations for {country_code} country and {payment_method} payment method is found and both should exist not either one."
            )
            
            query = f"{base_query} Use the following sample structure as reference: {metadata_structure} but return empty json when no configuration found for {country_code} country and {payment_method} payment method"

            logger.debug(f"Loading documents from {ASPNETMVC_APP_PATH}")
            documents = SimpleDirectoryReader(
                ASPNETMVC_APP_PATH,
                required_exts=[".cs"],
                recursive=True
            ).load_data()

            logger.info("Creating vector store index")
            index = VectorStoreIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            
            template = (
                "Context Information:\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Task: {query_str}\n"
                "Rules:\n"
                "Follow these rules:\n"
                f"1. Only include configurations that actually exist in the codebase\n"
                f"2. Do not make assumptions about configurations that are not present\n"
                f"3. If no specific configuration is found for the {country_code} country or {payment_method} payment method, return empty JSON\n"
                f"4. Include only the fields that are explicitly configured in the code"
                "Follow the response structure:"
                "explaation:"
                "---------------------\n"
                "{response_str}\n"
                "---------------------\n"
                "Answer:"
                "---------------------\n"
                "{response_str}\n"
                "----------------------------------\n"
                "If you don't know the answer, please do mention : I don't know!"            
            )
            
            query_engine.update_prompts(PromptTemplate(template=template))

            response = query_engine.query(query)
            logger.info("Successfully received response from query engine")
            logger.info(f"Raw response from query engine: {response}")

            result = self._extract_json(response.response)
            logger.info("Successfully extracted JSON from response")
            return result
        except Exception as e:
            logger.error(f"Error in Groq Ingest analysis: {str(e)}")
            raise RuntimeError(f"Error in Groq Ingest process: {e}")


