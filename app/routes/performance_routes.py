from flask import Blueprint, request, jsonify
from app.services.performance_service import PerformanceService
from app.utils.auth import require_api_key

performance_bp = Blueprint('performance_bp', __name__)

@performance_bp.route('/performance', methods=['POST'])
@require_api_key
def add_performance():
    data = request.get_json()
    try:
        perf = PerformanceService.add_performance(data)
        return jsonify({"message": "Performance added", "id": perf.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@performance_bp.route('/vendors/<int:vendor_id>/performance', methods=['GET'])
@require_api_key
def get_vendor_performance(vendor_id):
    history = PerformanceService.get_vendor_history(vendor_id)
    avg_score = PerformanceService.get_vendor_average(vendor_id)
    
    return jsonify({
        "average_score": round(avg_score, 2),
        "history": [{
            "month": p.month_date.isoformat(),
            "quality": p.quality_rating,
            "timeliness": p.timeliness_rating,
            "cost": p.cost_rating,
            "overall": p.overall_score
        } for p in history]
    }), 200

@performance_bp.route('/performance/top', methods=['GET'])
@require_api_key
def get_top_performers():
    top_vendors = PerformanceService.get_top_performers()
    return jsonify([{
        "vendor_id": v.vendor_id,
        "average_score": round(v.avg_score, 2)
    } for v in top_vendors]), 200
