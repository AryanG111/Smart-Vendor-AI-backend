from app.models.performance import VendorPerformance
from app.extensions import db
from sqlalchemy import func

class PerformanceService:
    @staticmethod
    def add_performance(data):
        overall_score = (data['quality_rating'] + data['timeliness_rating'] + data['cost_rating']) / 3.0
        
        new_perf = VendorPerformance(
            vendor_id=data['vendor_id'],
            month_date=data['month_date'],
            quality_rating=data['quality_rating'],
            timeliness_rating=data['timeliness_rating'],
            cost_rating=data['cost_rating'],
            overall_score=overall_score
        )
        db.session.add(new_perf)
        db.session.commit()
        return new_perf

    @staticmethod
    def get_vendor_history(vendor_id):
        return VendorPerformance.query.filter_by(vendor_id=vendor_id).order_by(VendorPerformance.month_date.desc()).all()

    @staticmethod
    def get_vendor_average(vendor_id):
        avg_score = db.session.query(func.avg(VendorPerformance.overall_score))\
            .filter_by(vendor_id=vendor_id).scalar()
        return avg_score or 0.0

    @staticmethod
    def get_top_performers(limit=5):
        # This is a simplified query. For more complex "overall" ranking, 
        # we might want to average scores per vendor first.
        # Here we just take the top individual monthly records or we can group by vendor.
        # Let's group by vendor and get average score.
        results = db.session.query(
            VendorPerformance.vendor_id, 
            func.avg(VendorPerformance.overall_score).label('avg_score')
        ).group_by(VendorPerformance.vendor_id)\
        .order_by(func.avg(VendorPerformance.overall_score).desc())\
        .limit(limit).all()
        
        return results
