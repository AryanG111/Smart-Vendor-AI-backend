from app.models.vendor import Vendor
from app.models.performance import VendorPerformance
from app.services.ai_service import ai_service
from app.extensions import db
from sqlalchemy import func

def recommend_vendors(purchase_description, request_category, top_n=5):
    # 1. Generate embedding for the purchase request
    request_embedding = ai_service.generate_embedding(purchase_description)
    
    # 2. Fetch all active vendors
    vendors = Vendor.query.filter_by(is_active=True).all()
    recommendations = []

    for vendor in vendors:
        vendor_emb = vendor.get_embedding()
        
        # Skip if no embedding (should regenerate via script)
        if not vendor_emb:
            continue

        # A. Text Similarity (Cosine)
        similarity_score = ai_service.compute_similarity(request_embedding, vendor_emb)

        # B. Performance Score (Average of all time)
        avg_perf = db.session.query(func.avg(VendorPerformance.overall_score))\
            .filter_by(vendor_id=vendor.id).scalar() or 0.0
        
        # Normalize performance (assume 0-10 scale, normalize to 0-1)
        norm_perf = avg_perf / 10.0 

        # C. Category Matching Bonus
        cat_bonus = 0.2 if vendor.category.lower() == request_category.lower() else 0.0

        # D. Final Combined Ranking Formula
        # Weights: 60% Description Match, 30% Performance, + Category Bonus
        final_score = (0.6 * similarity_score) + (0.3 * norm_perf) + cat_bonus

        recommendations.append({
            "vendor_id": vendor.id,
            "vendor_name": vendor.name,
            "similarity_score": round(float(similarity_score), 4),
            "average_performance": round(float(avg_perf), 2),
            "final_score": round(float(final_score), 4)
        })

    # Sort by Final Score descending
    recommendations.sort(key=lambda x: x['final_score'], reverse=True)
    
    return recommendations[:top_n]