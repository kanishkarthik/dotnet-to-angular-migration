import json
import re
from groq import Groq
from .base_llm_service import BaseLLMService
from config.constants import GROQ_API_KEY, GROQ_LARGE_LANGUAGE_MODEL, SAMPLE_METADATA_PATH
from utils.logger import logger

class GroqService(BaseLLMService):
    def __init__(self, llm_model: str):
        super().__init__()
        self.client = Groq(api_key=GROQ_API_KEY)
        self.llm_model = llm_model

    def analyze(self, content: str, custom_prompt: str = None) -> str:
        logger.info("Starting Groq analysis")
        try:
            # Define the prompt using a clear and standardized format
            prompt = ("""
                You are an expert in analyzing ASP.NET MVC configuration files and generating JSON metadata.
                Your task is to:
                - Analyze the provided ASP.NET MVC configuration file.
                - Generate JSON metadata to dynamically render fields in an Angular UI.
                - Provide the respective formId, country and payment method details
                - Ensure the JSON metadata follows this structure:
                {}
                - Consider any additional UI parameters that may enhance the UI rendering.
                - Include attributes only when necessary, avoiding redundant or empty properties.
                - Facilitate dynamic field rendering in Angular, supporting different input types (e.g., text, dropdown, radio buttons).

                ASP.NET MVC Configuration:
                {}

                Additional Context:
                {}
            """.format(self.metadata_structure, content, custom_prompt))

            # Log the request details for better traceability
            logger.info(f"Sending request to Groq API with content length: {len(content)}")
            logger.info(f"Prompt: {prompt}")

            # Send the request to the LLM with a clear role system
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert in ASP.NET MVC and Angular UI metadata generation."},
                    {"role": "user", "content": prompt}
                ],
                model=self.llm_model,
            )
            logger.info("Successfully received response from Groq API")
            logger.info(f"Raw response from Groq: {response.choices[0].message.content}")

            result = self._extract_json(response.choices[0].message.content)
            logger.info("Successfully extracted JSON from response")
            return result
        except Exception as e:
            logger.error(f"Error in Groq analysis: {str(e)}")
            raise RuntimeError(f"Error interacting with Groq API: {e}")

