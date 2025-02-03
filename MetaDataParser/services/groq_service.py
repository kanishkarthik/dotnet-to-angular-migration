import json
import re
from groq import Groq

from config.constants import GROQ_API_KEY, GROQ_LARGE_LANGUAGE_MODEL, SAMPLE_METADATA_PATH

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def analyze_with_groq(file_content):
    """Send the .cs file content to Groq API and get the JSON metadata."""
    try:
        metadata_structure = ''
        # read json as string config/metadata_sample.json
        with open(SAMPLE_METADATA_PATH, 'r') as file:
            # read json as string config/metadata_sample
            metadata_structure = file.read()
        # Define metadata structure explanation
        prompt = """Analyze the given ASP.NET MVC configuration file and generate JSON metadata 
        that can be used to dynamically render fields in an Angular UI. 

        The metadata format should match this structure, and you may need to consider additional UI parameters 
        that are not explicitly mentioned and provide attributes only when it is necessary:
        """
        asp_net_mvc_config = """
        Asp.NET MVC configuration(class based view engine):
        {}    
        """.format(file_content)
        # prompt + metadata_structure + asp_net_mvc_config

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt + metadata_structure + asp_net_mvc_config,
                }
            ],
            model=GROQ_LARGE_LANGUAGE_MODEL,
        )
        json_part = re.search(r'```json\n(.*?)```', chat_completion.choices[0].message.content, re.DOTALL)
        if json_part:
            json_text = json_part.group(0)
            # Remove ```json markers from the start and end
            cleaned_json = json_text.strip('```json\n').strip('```')
            try:
                return cleaned_json  # Return the cleaned JSON metadata
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
        else:
            print("No JSON found in the text.")
    except Exception as e:
        raise RuntimeError(f"Error interacting with Groq API: {e}")
