from flask import Flask, jsonify, request
from datetime import datetime
import logging
from app.config import Config
from app.extensions import db

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    
    # Import Models to register them with SQLAlchemy
    from app.models import vendor, performance, feedback, purchase_request

    # Import Blueprints
    from app.routes.vendor_routes import vendor_bp
    from app.routes.performance_routes import performance_bp
    from app.routes.purchase_routes import purchase_bp
    from app.routes.feedback_routes import feedback_bp
    from app.routes.health_routes import health_bp
    
    # Register Blueprints
    app.register_blueprint(vendor_bp)
    app.register_blueprint(performance_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(health_bp)
    
    # Request Logging Hook
    @app.before_request
    def log_request_info():
        if request.path != '/health' and request.path != '/readiness':
            logger.info(f"Request: {datetime.utcnow()} | {request.method} {request.path} | IP: {request.remote_addr}")

    @app.after_request
    def log_response_info(response):
        if request.path != '/health' and request.path != '/readiness':
            logger.info(f"Response: {response.status} | {request.method} {request.path}")
        return response

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
        logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        return jsonify({"error": "Unexpected Error", "message": str(e)}), 500

    return app