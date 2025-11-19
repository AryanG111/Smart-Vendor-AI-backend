from app.extensions import db
from datetime import datetime

class VendorPerformance(db.Model):
    __tablename__ = 'vendor_performance'

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False, index=True)
    month_date = db.Column(db.Date, nullable=False) # e.g., 2023-11-01
    
    quality_rating = db.Column(db.Float, nullable=False)
    timeliness_rating = db.Column(db.Float, nullable=False)
    cost_rating = db.Column(db.Float, nullable=False)
    
    # Calculated: (Quality + Timeliness + Cost) / 3
    overall_score = db.Column(db.Float, nullable=False)