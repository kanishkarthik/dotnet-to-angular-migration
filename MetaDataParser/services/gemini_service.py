import json
import re
import google.generativeai as genai
from config.constants import GEMINI_API_KEY, GEMINI_MODEL, SAMPLE_METADATA_PATH

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def analyze_with_gemini(file_content):
    """Send the .cs file content to Gemini AI and get JSON metadata."""
    try:
        # Read sample metadata structure
        with open(SAMPLE_METADATA_PATH, 'r') as file:
            metadata_structure = file.read()

        # Define prompt
        prompt = f"""Analyze the given ASP.NET MVC configuration file and generate JSON metadata 
        that can be used to dynamically render fields in an Angular UI.

        The metadata format should match this structure, and you may need to consider additional UI parameters 
        that are not explicitly mentioned and provide attributes only when necessary.

        Sample Metadata:
        {metadata_structure}

        ASP.NET MVC Configuration (Class-based view engine):
        {file_content}
        """

        # Call Gemini AI API
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        json_part = re.search(r'```json\n(.*?)```', response.text, re.DOTALL)
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
        raise RuntimeError(f"Error interacting with Gemini AI: {e}")
