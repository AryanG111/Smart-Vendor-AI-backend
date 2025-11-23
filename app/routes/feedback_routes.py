from flask import Blueprint, request, jsonify
from app.services.feedback_service import FeedbackService
from app.utils.auth import require_api_key

feedback_bp = Blueprint('feedback_bp', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
@require_api_key
def submit_feedback():
    data = request.get_json()
    try:
        feedback = FeedbackService.submit_feedback(data)
        return jsonify({
            "message": "Feedback submitted", 
            "id": feedback.id,
            "sentiment": feedback.sentiment_label
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@feedback_bp.route('/vendors/<int:vendor_id>/feedback', methods=['GET'])
@require_api_key
def get_vendor_feedback(vendor_id):
    feedbacks = FeedbackService.get_vendor_feedback(vendor_id)
    return jsonify([{
        "id": f.id,
        "text": f.feedback_text,
        "sentiment": f.sentiment_label,
        "created_at": f.created_at.isoformat()
    } for f in feedbacks]), 200
