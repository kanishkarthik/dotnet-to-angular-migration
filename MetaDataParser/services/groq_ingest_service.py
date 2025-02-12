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
        super().__init__()
        self.llm = Groq(model=GROQ_LARGE_LANGUAGE_MODEL, api_key=GROQ_API_KEY)
        self.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
        self._setup_settings()

    def _setup_settings(self):
        Settings.llm = self.llm
        Settings.num_output = 250
        Settings.embed_model = self.embed_model

    def analyze(self, country_code: str, payment_method: str) -> str:
        query = f"Generate JSON metadata based on {country_code} and {payment_method}"
        query = f"{query} and the sample json is {self.metadata_structure}"

        documents = SimpleDirectoryReader(
            ASPNETMVC_APP_PATH,
            required_exts=[".cs"],
            recursive=True
        ).load_data()

        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        
        template = (
            "We have provided context information below. \n"
            "---------------------\n"
            "{context_str}"
            "\n---------------------\n"
            "Given this information, please answer the question: {query_str}\n"
            "If you don't know the answer, please do mention : I don't know !"
        )
        
        query_engine.update_prompts(PromptTemplate(template=template))
        response = query_engine.query(query).response
        return self._extract_json(response)


