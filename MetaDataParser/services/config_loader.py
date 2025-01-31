import json
import os
from config.constants import ASPNETMVC_CONFIG_FILE

def load_configurations():
    """Load the configurations from the configurations.json file."""
    if not os.path.exists(ASPNETMVC_CONFIG_FILE):
        raise FileNotFoundError(f"{ASPNETMVC_CONFIG_FILE} not found!")
    
    with open(ASPNETMVC_CONFIG_FILE, "r") as f:
        return json.load(f)
