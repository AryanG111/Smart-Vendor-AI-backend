from flask import Flask, jsonify
from datetime import datetime
from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)

    # Import Blueprints
    from app.routes.vendor_routes import vendor_bp
    # form app.routes.performance_routes import performance_bp (Implement similarly)
    
    # Register Blueprints
    app.register_blueprint(vendor_bp)
    
    # Health & Readiness Endpoints
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "timestamp": datetime.utcnow()}), 200

    @app.route('/readiness', methods=['GET'])
    def readiness_check():
        try:
            # Check DB connection
            db.session.execute('SELECT 1')
            return jsonify({"status": "ready", "database": "connected"}), 200
        except Exception as e:
            return jsonify({"status": "not ready", "error": str(e)}), 503

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found", "message": "The requested resource does not exist"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "message": "Something went wrong on the server"}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all other unhandled exceptions"""
        return jsonify({"error": "Unexpected Error", "message": str(e)}), 500

    return app