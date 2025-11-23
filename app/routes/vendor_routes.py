from flask import Blueprint, request, jsonify
from app.services.vendor_service import VendorService
from app.services.recommendation_service import recommend_vendors
from app.utils.auth import require_api_key

vendor_bp = Blueprint('vendor_bp', __name__)

@vendor_bp.route('/vendors', methods=['POST'])
@require_api_key
def create_vendor():
    data = request.get_json()
    try:
        vendor = VendorService.create_vendor(data)
        return jsonify({"message": "Vendor created", "id": vendor.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@vendor_bp.route('/vendors', methods=['GET'])
@require_api_key
def get_vendors():
    category = request.args.get('category')
    active_only = request.args.get('active_only') == 'true'
    vendors = VendorService.get_all_vendors(category, active_only)
    return jsonify([v.to_dict() for v in vendors]), 200

@vendor_bp.route('/vendors/<int:vendor_id>', methods=['GET'])
@require_api_key
def get_vendor(vendor_id):
    vendor = VendorService.get_vendor_by_id(vendor_id)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    return jsonify(vendor.to_dict()), 200

@vendor_bp.route('/vendors/<int:vendor_id>', methods=['PUT'])
@require_api_key
def update_vendor(vendor_id):
    data = request.get_json()
    vendor = VendorService.update_vendor(vendor_id, data)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    return jsonify({"message": "Vendor updated", "vendor": vendor.to_dict()}), 200

@vendor_bp.route('/vendors/<int:vendor_id>', methods=['DELETE'])
@require_api_key
def delete_vendor(vendor_id):
    success = VendorService.delete_vendor(vendor_id)
    if not success:
        return jsonify({"error": "Vendor not found"}), 404
    return jsonify({"message": "Vendor deleted"}), 200

@vendor_bp.route('/vendors/recommend', methods=['POST'])
@require_api_key
def recommend():    
    data = request.get_json()
    results = recommend_vendors(
        purchase_description=data['description'],
        request_category=data['category']
    )
    return jsonify(results), 200