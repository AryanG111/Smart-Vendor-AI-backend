from app.extensions import db

class VendorFeedback(db.Model):
    __tablename__ = 'vendor_feedback'

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    sentiment_label = db.Column(db.String(20)) # Positive, Negative, Neutral
    created_at = db.Column(db.DateTime, default=db.func.now())