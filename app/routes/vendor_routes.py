from flask import Blueprint, request, jsonify
from app.models.vendor import Vendor
from app.extensions import db
from app.utils.auth import require_api_key
from app.services.ai_service import ai_service

vendor_bp = Blueprint('vendor_bp', __name__)

@vendor_bp.route('/vendors', methods=['POST'])
@require_api_key
def create_vendor():
    data = request.get_json()
    
    # Generate embedding immediately upon creation
    embedding = ai_service.generate_embedding(f"{data['category']} {data['description']}")
    
    new_vendor = Vendor(
        name=data['name'],
        category=data['category'],
        description=data['description'],
        contact_email=data.get('contact_email')
    )
    new_vendor.set_embedding(embedding)
    
    db.session.add(new_vendor)
    db.session.commit()
    
    return jsonify({"message": "Vendor created", "id": new_vendor.id}), 201

@vendor_bp.route('/vendors/recommend', methods=['POST'])
@require_api_key
def recommend():
    from app.services.recommendation_service import recommend_vendors
    data = request.get_json()
    
    results = recommend_vendors(
        purchase_description=data['description'],
        request_category=data['category']
    )
    
    return jsonify(results), 200