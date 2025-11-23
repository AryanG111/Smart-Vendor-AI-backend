from flask import Blueprint, request, jsonify
from app.services.purchase_service import PurchaseService
from app.utils.auth import require_api_key

purchase_bp = Blueprint('purchase_bp', __name__)

@purchase_bp.route('/purchase-requests', methods=['POST'])
@require_api_key
def create_request():
    data = request.get_json()
    try:
        req = PurchaseService.create_request(data)
        return jsonify({"message": "Purchase request created", "id": req.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@purchase_bp.route('/purchase-requests', methods=['GET'])
@require_api_key
def get_requests():
    requests = PurchaseService.get_all_requests()
    return jsonify([r.to_dict() for r in requests]), 200

@purchase_bp.route('/purchase-requests/<int:req_id>', methods=['GET'])
@require_api_key
def get_request(req_id):
    req = PurchaseService.get_request_by_id(req_id)
    if not req:
        return jsonify({"error": "Request not found"}), 404
    return jsonify(req.to_dict()), 200
