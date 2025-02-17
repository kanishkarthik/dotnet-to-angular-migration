import os

# Groq API Key and Endpoint
GROQ_API_KEY = "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"
# "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"

# Groq (LLM)
GROQ_LARGE_LANGUAGE_MODEL = "llama-3.3-70b-versatile"

# Gemini API Key
GEMINI_API_KEY = "AIzaSyANB3nTAyUGRfMmpYQp73hI-3ZUyAp5Q-k"

# OpenAI API Key
OPENAI_API_KEY = "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"

# Gemini Model
GEMINI_MODEL = "gemini-1.5-pro-latest"

# App Root Path
ROOT_PATH = os.path.dirname(__file__).replace('\MetaDataParser\config', '')

# Angular App - Metadata Path
ANGULAR_APP_METADATA_PATH = os.path.join(ROOT_PATH, "AngularApp", "src", "assets", "metadata")

# ASP.NET MVC Configurations File
ASPNETMVC_CONFIG_FILE = os.path.join(ROOT_PATH, "DotNetApp", "configurations.json")
ASPNETMVC_APP_CONFIG_PATH = os.path.join(ROOT_PATH, "DotNetApp", "ViewConfigurations")
ASPNETMVC_APP_PATH = os.path.join(ROOT_PATH, "DotNetApp")
SAMPLE_METADATA_PATH = os.path.join(ROOT_PATH,'MetaDataParser', 'config', 'sample_metadata.json')
# Log Directory Path
LOG_DIR_PATH = os.path.join(ROOT_PATH, 'logs')

# Index Storage Path
INDEX_STORAGE_PATH = os.path.join(ROOT_PATH, 'storage', 'vector_index')

# Chroma Db Path
CHROMA_DB_PATH = os.path.join(ROOT_PATH, 'storage', 'chroma_db')
