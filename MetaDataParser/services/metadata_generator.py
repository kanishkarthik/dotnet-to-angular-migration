import os
from typing import Optional

from services.gemini_service import GeminiService
from services.groq_ingest_service import GroqIngestService
from services.groq_service import GroqService
from utils.logger import logger

class MetadataGenerator:
    def __init__(self, config: dict, aspnet_path: str, angular_path: str):
        self.config = config
        self.aspnet_path = aspnet_path
        self.angular_path = angular_path

    def generate(self, country_code: str, payment_method: str, ai_model: str) -> str:
        logger.info(f"Starting metadata generation for country: {country_code}, payment method: {payment_method}, AI model: {ai_model}")
        key = f"{country_code.lower()}_{payment_method.lower()}"
        file_content = ''
        try:
            if ai_model != 'groq_ingest':
                config = self.config.get(key)
                if not config:
                    logger.error(f"No configuration found for {key}")
                    raise ValueError(f"No configuration found for {key}")

                file_content = self._read_cs_file(config.get("config_path"))
            metadata = self._analyze_content(file_content, ai_model, country_code, payment_method)
            self._save_metadata(key, metadata)
            logger.info(f"Successfully generated metadata for {key}")
            return metadata
        except Exception as e:
            logger.error(f"Error generating metadata: {str(e)}")
            raise

    def _read_cs_file(self, relative_path: str) -> str:
        logger.info(f"Reading C# file from: {relative_path}")
        file_path = os.path.join(self.aspnet_path, relative_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found at {file_path}")
        with open(file_path, "r") as f:
            return f.read()

    def _analyze_content(self, content: str, ai_model: str, country_code: str, payment_method: str) -> str:
        logger.info(f"Analyzing content using {ai_model}")
        if ai_model == 'groq':
            return GroqService().analyze(content)
        elif ai_model == 'groq_ingest':
            return GroqIngestService().analyze(country_code, payment_method)
        elif ai_model == 'gemini':
            return GeminiService().analyze(content)
        else:
            raise ValueError(f"Unsupported AI model: {ai_model}")

    def _save_metadata(self, key: str, metadata: str) -> None:
        logger.info(f"Saving metadata for key: {key}")
        output_path = os.path.join(self.angular_path, f"{key}.json")
        with open(output_path, "w") as f:
            f.write(metadata)
