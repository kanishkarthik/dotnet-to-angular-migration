import json
import re
import google.generativeai as genai
from .base_llm_service import BaseLLMService
from config.constants import GEMINI_API_KEY, GEMINI_MODEL, SAMPLE_METADATA_PATH
from utils.logger import logger

class GeminiService(BaseLLMService):
    def __init__(self, llm_model: str):
        super().__init__()
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(llm_model)

    def analyze(self, content: str, custom_prompt: str = None) -> str:
        logger.info("Starting Gemini analysis")
        try:
            base_prompt = """Analyze the given ASP.NET MVC configuration file and generate JSON metadata 
            that can be used to dynamically render fields in an Angular UI."""

            if custom_prompt:
                base_prompt = "{}{}.".format(base_prompt, custom_prompt)

            prompt = f"""{base_prompt}

            The metadata format should match this structure, and you may need to consider additional UI parameters 
            that are not explicitly mentioned and provide attributes only when necessary.

            Sample Metadata:
            {self.metadata_structure}

            ASP.NET MVC Configuration:
            {content}
            """

            logger.info(f"Sending request to Gemini API with content length: {len(content)}")
            response = self.model.generate_content(prompt)
            logger.info("Successfully received response from Gemini API")
            logger.info(f"Raw response from Gemini: {response.text}")

            result = self._extract_json(response.text)
            logger.info("Successfully extracted JSON from response")
            return result
        except Exception as e:
            logger.error(f"Error in Gemini analysis: {str(e)}")
            raise RuntimeError(f"Error interacting with Gemini AI: {e}")
