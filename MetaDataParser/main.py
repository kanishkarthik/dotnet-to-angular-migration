from flask import Flask, render_template, request, jsonify
from config.constants import ANGULAR_APP_METADATA_PATH, ASPNETMVC_APP_PATH
from services.config_loader import load_configurations
from services.metadata_generator import MetadataGenerator
from decorators import handle_errors

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
    country_code = request.form.get("country_code")
    payment_method = request.form.get("payment_method")
    ai_model = request.form.get("ai_model")

    if not all([country_code, payment_method, ai_model]):
        raise ValueError("Country code, payment method, and AI model are required!")

    metadata = metadata_generator.generate(country_code, payment_method, ai_model)
    return jsonify({"metadata": metadata})

if __name__ == "__main__":
    app.run(debug=True)
