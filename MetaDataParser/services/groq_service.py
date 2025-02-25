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
            base_prompt = """Analyze the given ASP.NET MVC configuration file and generate JSON metadata 
            that can be used to dynamically render fields in an Angular UI. 

            The metadata format should match this structure, and you may need to consider additional UI parameters 
            that are not explicitly mentioned and provide attributes only when it is necessary:
            """
            
            if custom_prompt:
                base_prompt = "{}{}.".format(base_prompt, custom_prompt)

            full_prompt = base_prompt + self.metadata_structure + f"\nAsp.NET MVC configuration:\n{content}"

            logger.info(f"Sending request to Groq API with content length: {len(content)}")
            logger.info(f"Prompt: {full_prompt}")
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
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

