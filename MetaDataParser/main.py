from flask import Flask, render_template, request, jsonify
from config.constants import ANGULAR_APP_METADATA_PATH, ASPNETMVC_APP_PATH
from services.config_loader import load_configurations
from services.metadata_generator import MetadataGenerator
from decorators import handle_errors
from utils.logger import logger

app = Flask(__name__)
CONFIGURATIONS = load_configurations()
metadata_generator = MetadataGenerator(
    CONFIGURATIONS,
    ASPNETMVC_APP_PATH,
    ANGULAR_APP_METADATA_PATH
)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/generate-metadata", methods=["POST"])
@handle_errors
def generate_metadata():
    logger.info("Received metadata generation request")
    country_code = request.form.get("country_code")
    payment_method = request.form.get("payment_method")
    ai_model = request.form.get("ai_model")
    llm_model = request.form.get("llm_model")

    logger.info(f"Request parameters - Country: {country_code}, Payment Method: {payment_method}, AI Model: {ai_model}")

    if not all([country_code, payment_method, ai_model]):
        logger.error("Missing required parameters")
        raise ValueError("Country code, payment method, and AI model are required!")

    try:
        metadata = metadata_generator.generate(country_code, payment_method, ai_model, llm_model)
        logger.info("Successfully generated metadata,"+metadata)
        return jsonify({"metadata": metadata})
    except Exception as e:
        logger.error(f"Error in generate_metadata endpoint: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(debug=True)
