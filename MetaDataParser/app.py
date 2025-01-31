import os
import json
import re
from flask import Flask, render_template, request, jsonify
from groq import Groq

# Flask app initialization
app = Flask(__name__)

# Groq API Key and Endpoint
GROQ_API_KEY = "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"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"  # Replace with the actual endpoint if different.
client = Groq(api_key=GROQ_API_KEY)

# App Root Path
ROOT_PATH = os.path.dirname(__file__).replace('MetaDataParser', '')

# Angular App - Metadata Path
ANGULAR_APP_METADATA_PATH = ROOT_PATH + "AngularApp\\src\\assets\\metadata"

# Load configurations.json
ASPNETMVC_CONFIG_FILE = ROOT_PATH + "DotNetApp\configurations.json"
if not os.path.exists(ASPNETMVC_CONFIG_FILE):
    raise FileNotFoundError(f"{ASPNETMVC_CONFIG_FILE} not found!")

with open(ASPNETMVC_CONFIG_FILE, "r") as f:
    CONFIGURATIONS = json.load(f)


def read_cs_file(file_path):
    """Read the content of the .cs file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found at {file_path}")
    with open(file_path, "r") as f:
        return f.read()


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
                # Parse the JSON to validate and format it
                return (cleaned_json)
                # parsed_json = json.loads(cleaned_json)
                # print(json.dumps(parsed_json, indent=4))
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
        else:
            print("No JSON found in the text.")
    except Exception as e:
        raise RuntimeError(f"Error interacting with Groq API: {e}")


@app.route("/")
def index():
    """Render the input form for country code and payment method."""
    return render_template("index.html")


@app.route("/generate-metadata", methods=["POST"])
def generate_metadata():
    """Generate JSON metadata based on user input."""
    country_code = request.form.get("country_code")
    payment_method = request.form.get("payment_method")

    if not country_code or not payment_method:
        return jsonify({"error": "Country code and payment method are required!"}), 400

    # Locate the configuration file
    key = f"{country_code.lower()}_{payment_method.lower()}"
    config = CONFIGURATIONS.get(key)
    if not config:
        return jsonify({"error": f"No configuration found for {key}!"}), 404

    config_path = config.get("config_path")    
    try:
        # Read .cs file content
        file_content = read_cs_file(config_path)
        print(file_content)
        # Analyze content using Groq
        metadata = analyze_with_groq(file_content)
        # write metadata in below ANGULAR_APP_METADATA_PATH
        with open(os.path.join(ANGULAR_APP_METADATA_PATH, f"{key}.json"), "w") as f:
            f.write(metadata)
        return jsonify({"metadata": (metadata)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
