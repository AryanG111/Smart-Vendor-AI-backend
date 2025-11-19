from functools import wraps
from flask import request, jsonify, current_app
import os

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        valid_key = os.getenv('API_KEY', 'my-secret-key')
        
        if not api_key or api_key != valid_key:
            return jsonify({"error": "Unauthorized", "message": "Invalid or missing API Key"}), 401
            
        return f(*args, **kwargs)
    return decorated_function