import os

# Groq API Key and Endpoint
GROQ_API_KEY = "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"

# App Root Path
ROOT_PATH = os.path.dirname(__file__).replace('\MetaDataParser\config', '')

# Angular App - Metadata Path
ANGULAR_APP_METADATA_PATH = os.path.join(ROOT_PATH, "AngularApp", "src", "assets", "metadata")

# ASP.NET MVC Configurations File
ASPNETMVC_CONFIG_FILE = os.path.join(ROOT_PATH, "DotNetApp", "configurations.json")
ASPNETMVC_APP_PATH = os.path.join(ROOT_PATH, "DotNetApp", "ViewConfigurations")
