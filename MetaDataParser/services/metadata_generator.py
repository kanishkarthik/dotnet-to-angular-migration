import os
from typing import Optional

from services.gemini_service import GeminiService
from services.groq_ingest_service import GroqIngestService
from services.groq_service import GroqService

class MetadataGenerator:
    def __init__(self, config: dict, aspnet_path: str, angular_path: str):
        self.config = config
        self.aspnet_path = aspnet_path
        self.angular_path = angular_path

    def generate(self, country_code: str, payment_method: str, ai_model: str) -> str:
        key = f"{country_code.lower()}_{payment_method.lower()}"
        file_content = ''
        if ai_model != 'groq_ingest':
            config = self.config.get(key)
            
            if not config:
                raise ValueError(f"No configuration found for {key}")

            file_content = self._read_cs_file(config.get("config_path"))
        metadata = self._analyze_content(file_content, ai_model, country_code, payment_method)
        
        self._save_metadata(key, metadata)
        return metadata

    def _read_cs_file(self, relative_path: str) -> str:
        file_path = os.path.join(self.aspnet_path, relative_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found at {file_path}")
        with open(file_path, "r") as f:
            return f.read()

    def _analyze_content(self, content: str, ai_model: str, country_code: str, payment_method: str) -> str:
        if ai_model == 'groq':
            return GroqService().analyze(content)
        elif ai_model == 'groq_ingest':
            return GroqIngestService().analyze(country_code, payment_method)
        elif ai_model == 'gemini':
            return GeminiService().analyze(content)
        else:
            raise ValueError(f"Unsupported AI model: {ai_model}")

    def _save_metadata(self, key: str, metadata: str) -> None:
        output_path = os.path.join(self.angular_path, f"{key}.json")
        with open(output_path, "w") as f:
            f.write(metadata)
