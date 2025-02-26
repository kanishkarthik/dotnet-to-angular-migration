import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv()

# Groq API Key and Endpoint
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq (LLM)
GROQ_LARGE_LANGUAGE_MODEL = "llama-3.3-70b-versatile"

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
INDEX_STORAGE_PATH_2 = os.path.join(ROOT_PATH, 'storage', 'vector_index_2')

# Chroma Db Path
CHROMA_DB_PATH = os.path.join(ROOT_PATH, 'storage', 'chroma_db')
