from flask import Flask, render_template, request, jsonify
from config.constants import ANGULAR_APP_METADATA_PATH, ASPNETMVC_APP_CONFIG_PATH
from services.config_loader import load_configurations
from services.metadata_generator import MetadataGenerator
from decorators import handle_errors
from utils.logger import logger

app = Flask(__name__)
CONFIGURATIONS = load_configurations()
metadata_generator = MetadataGenerator(
    CONFIGURATIONS,
    ASPNETMVC_APP_CONFIG_PATH,
    ANGULAR_APP_METADATA_PATH
)
@app.route("/")
def index():
    return render_template("landing.html", active_page='home')

@app.route("/metadata")
def metadata_page():
    return render_template("main.html", active_page='metadata')


@app.route("/generate-metadata", methods=["POST"])
@handle_errors
def generate_metadata():
    logger.info("Received metadata generation request")
    country_code = request.form.get("country_code")
    payment_method = request.form.get("payment_method")
    ai_model = request.form.get("ai_model")
    llm_model = request.form.get("llm_model")
    custom_prompt = request.form.get("custom_prompt")
    re_index = request.form.get("re_index")
    re_index = True if re_index == "true" else False
    save_metadata = request.form.get("save_metadata")
    save_metadata = True if save_metadata == "true" else False

    logger.info(f"Request parameters - Country: {country_code}, Payment Method: {payment_method}, AI Model: {ai_model}, Custom Prompt: {custom_prompt}")

    if not all([country_code, payment_method, ai_model]):
        logger.error("Missing required parameters")
        raise ValueError("Country code, payment method, and AI model are required!")

    try:
        metadata = metadata_generator.generate(country_code, payment_method, ai_model, llm_model, re_index, save_metadata, custom_prompt)
        logger.info("Successfully generated metadata")
        return jsonify({"metadata": metadata})
    except Exception as e:
        logger.error(f"Error in generate_metadata endpoint: {str(e)}")
        raise

@app.route("/save-metadata", methods=["POST"])
@handle_errors
def save_metadata():
    logger.info("Received save metadata request")
    try:
        metadata = request.json.get('metadata')
        key = request.json.get('key')
        
        if not key:
            raise ValueError("No key provided")
        if not metadata:
            raise ValueError("No metadata provided")
        key = str(key).lower()        
        metadata_generator._save_metadata(key, metadata)
        logger.info("Successfully saved metadata")
        return jsonify({"message": "Metadata saved successfully"}), 200
    except Exception as e:
        logger.error(f"Error in save_metadata endpoint: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(debug=True)
