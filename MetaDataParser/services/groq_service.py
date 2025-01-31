import json
import re
from groq import Groq
from config.constants import GROQ_API_KEY

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def analyze_with_groq(file_content):
    """Send the .cs file content to Groq API and get the JSON metadata."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Analyze the given ASP.NET MVC configuration file and generate JSON metadata "
                        "that can be used to dynamically render fields in an Angular UI. The metadata format should match this structure and you may need to consider other UI params which not mentioned: "
                        '{"sections": [{"section": "sectionName", "title": "Section Title", "fields": [{"field": "fieldName", "label": "Field Label", "type": "FieldType", "required": true|false}]}]}.\n\nFile content:\n\n'
                        + file_content
                    ),
                }
            ],
            model="llama-3.3-70b-versatile",
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
