from flask import Flask, render_template, request, jsonify
from config.constants import ANGULAR_APP_METADATA_PATH, ASPNETMVC_APP_CONFIG_PATH
from services.config_loader import load_configurations
from services.metadata_generator import MetadataGenerator
from decorators import handle_errors
from utils.logger import logger
from services.ollama_service import OllamaRAGService

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

@app.route("/ollama")
def ollama_page():
    return render_template("ollama.html", active_page='ollama')

@app.route("/api/ollama", methods=["POST"])
@handle_errors
def process_ollama_request():
    data = request.json
    model_name = data.get("model_name")
    prompt = data.get("prompt")
    context = data.get("context")

    if not all([model_name, prompt]):
        raise ValueError("Model name and prompt are required!")

    try:
        ollama_service = OllamaRAGService(model_name)
        response = ollama_service.generate_response(prompt, context)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error in Ollama processing: {str(e)}")
        raise

@app.route("/generate-metadata", methods=["POST"])
@handle_errors
def generate_metadata():
    logger.info("Received metadata generation request")
    country_code = request.form.get("country_code")
    payment_method = request.form.get("payment_method")
    ai_model = request.form.get("ai_model")
    llm_model = request.form.get("llm_model")
    custom_prompt = request.form.get("custom_prompt")

    logger.info(f"Request parameters - Country: {country_code}, Payment Method: {payment_method}, AI Model: {ai_model}, Custom Prompt: {custom_prompt}")

    if not all([country_code, payment_method, ai_model]):
        logger.error("Missing required parameters")
        raise ValueError("Country code, payment method, and AI model are required!")

    try:
        metadata = metadata_generator.generate(country_code, payment_method, ai_model, llm_model, custom_prompt)
        logger.info("Successfully generated metadata")
        return jsonify({"metadata": metadata})
    except Exception as e:
        logger.error(f"Error in generate_metadata endpoint: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(debug=True)
