import os

# Groq API Key and Endpoint
GROQ_API_KEY = "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"
# "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"

# Groq (LLM)
GROQ_LARGE_LANGUAGE_MODEL = "llama-3.3-70b-versatile"

# Gemini API Key
GEMINI_API_KEY = "AIzaSyANB3nTAyUGRfMmpYQp73hI-3ZUyAp5Q-k"

# Gemini Model
GEMINI_MODEL = "gemini-1.5-pro-latest"

# App Root Path
ROOT_PATH = os.path.dirname(__file__).replace('\MetaDataParser\config', '')

# Angular App - Metadata Path
ANGULAR_APP_METADATA_PATH = os.path.join(ROOT_PATH, "AngularApp", "src", "assets", "metadata")

# ASP.NET MVC Configurations File
ASPNETMVC_CONFIG_FILE = os.path.join(ROOT_PATH, "DotNetApp", "configurations.json")
ASPNETMVC_APP_PATH = os.path.join(ROOT_PATH, "DotNetApp", "ViewConfigurations")
SAMPLE_METADATA_PATH = os.path.join(ROOT_PATH,'MetaDataParser', 'config', 'sample_metadata.json')

# Index Storage Path
INDEX_STORAGE_PATH = os.path.join(ROOT_PATH, 'storage', 'vector_index')
