import json
import re
import google.generativeai as genai
from .base_llm_service import BaseLLMService
from config.constants import GEMINI_API_KEY, GEMINI_MODEL, SAMPLE_METADATA_PATH

class GeminiService(BaseLLMService):
    def __init__(self):
        super().__init__()
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def analyze(self, content: str) -> str:
        try:
            prompt = f"""Analyze the given ASP.NET MVC configuration file and generate JSON metadata 
            that can be used to dynamically render fields in an Angular UI.

            The metadata format should match this structure, and you may need to consider additional UI parameters 
            that are not explicitly mentioned and provide attributes only when necessary.

            Sample Metadata:
            {self.metadata_structure}

            ASP.NET MVC Configuration:
            {content}
            """

            response = self.model.generate_content(prompt)
            return self._extract_json(response.text)
        except Exception as e:
            raise RuntimeError(f"Error interacting with Gemini AI: {e}")
