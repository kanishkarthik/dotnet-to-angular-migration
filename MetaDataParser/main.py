from flask import Flask, render_template, request, jsonify
from config.constants import ANGULAR_APP_METADATA_PATH, ASPNETMVC_APP_CONFIG_PATH
from services.config_loader import load_configurations
from services.metadata_generator import MetadataGenerator
from decorators import handle_errors
from utils.logger import logger
from services.ollama_service import OllamaService
from services.train_model import ModelTrainer

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

@app.route("/train")
@handle_errors
def train_model():
    return render_template("train.html", active_page='train')

@app.route("/ollama")
def ollama_page():
    return render_template("ollama.html", active_page='ollama')

@app.route("/api/ollama", methods=["POST"])
@handle_errors
def process_ollama_request():
    data = request.json
    model_name = data.get("model_name")
    embedding_model = data.get("embedding_model")
    prompt = data.get("prompt")
    context = data.get("context")

    if not all([model_name, prompt]):
        raise ValueError("Model name and prompt are required!")

    try:
        ollama_service = OllamaService(llm_model=model_name)
        response = ollama_service.analyze(prompt)
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

@app.route("/api/train", methods=["POST"])
@handle_errors
def start_training():
    logger.info("Received model training request")
    data = request.json
    base_model = data.get("base_model")
    epochs = int(data.get("epochs", 5))
    batch_size = int(data.get("batch_size", 2))
    learning_rate = float(data.get("learning_rate", 1e-5))

    if not base_model:
        raise ValueError("Base model selection is required!")

    try:
        trainer = ModelTrainer()
        trainer.train_model(epochs=epochs, batch_size=batch_size, learning_rate=learning_rate)
        return jsonify({"status": "success", "message": "Model training completed successfully"})
    except Exception as e:
        logger.error(f"Error in model training: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(debug=True)
