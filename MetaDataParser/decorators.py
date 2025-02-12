from functools import wraps
from flask import jsonify

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    return wrapper
