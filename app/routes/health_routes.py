from flask import Blueprint, jsonify
from app.extensions import db
from sqlalchemy import text

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@health_bp.route('/readiness', methods=['GET'])
def readiness_check():
    try:
        # Check DB connection
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "ready", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503
