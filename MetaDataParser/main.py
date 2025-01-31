import os
from flask import Flask, render_template, request, jsonify
from config.constants import ANGULAR_APP_METADATA_PATH, ASPNETMVC_APP_PATH
from services.groq_service import analyze_with_groq
from services.config_loader import load_configurations

# Flask app initialization
app = Flask(__name__)

# Load configurations
CONFIGURATIONS = load_configurations()

@app.route("/")
def index():
    """Render the input form for country code and payment method."""
    return render_template("main.html")

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

    config_path = os.path.join(ASPNETMVC_APP_PATH, config.get("config_path"))
    print(config_path, "config_path")
    try:
        # Read .cs file content
        file_content = read_cs_file(config_path)
        # Analyze content using Groq
        metadata = analyze_with_groq(file_content)
        
        # Write metadata to the Angular App directory
        with open(os.path.join(ANGULAR_APP_METADATA_PATH, f"{key}.json"), "w") as f:
            f.write(metadata)

        return jsonify({"metadata": metadata})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def read_cs_file(file_path):
    print("Reading cs file", file_path)
    """Read the content of the .cs file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found at {file_path}")
    with open(file_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True)
