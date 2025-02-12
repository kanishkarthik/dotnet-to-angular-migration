from abc import ABC, abstractmethod
import json
import re
from config.constants import SAMPLE_METADATA_PATH

class BaseLLMService(ABC):
    def __init__(self):
        self.metadata_structure = self._load_metadata_structure()

    def _load_metadata_structure(self) -> str:
        with open(SAMPLE_METADATA_PATH, 'r') as file:
            return file.read()

    def _extract_json(self, response_text: str) -> str:
        json_part = re.search(r'```json\n(.*?)```', response_text, re.DOTALL)
        if json_part:
            json_text = json_part.group(0)
            cleaned_json = json_text.strip('```json\n').strip('```')
            try:
                return cleaned_json
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
        print("No JSON found in the text.")
        return ""

    @abstractmethod
    def analyze(self, content: str) -> str:
        pass
    @abstractmethod
    def analyze(self, country_code: str, payment_method: str) -> str:
        pass
