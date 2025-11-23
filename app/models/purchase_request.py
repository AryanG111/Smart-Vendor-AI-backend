from app.extensions import db
from datetime import datetime

class PurchaseRequest(db.Model):
    __tablename__ = 'purchase_requests'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    urgency = db.Column(db.String(20), nullable=False) # Low, Medium, High
    budget = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'description': self.description,
            'urgency': self.urgency,
            'budget': self.budget,
            'created_at': self.created_at.isoformat()
        }
