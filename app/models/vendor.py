import json
from app.extensions import db
from datetime import datetime

class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    contact_email = db.Column(db.String(100), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Storing embedding as a JSON string (e.g., "[0.1, 0.5, ...]")
    embedding_json = db.Column(db.Text, nullable=True)

    # Relationships
    performances = db.relationship('VendorPerformance', backref='vendor', lazy=True)
    feedbacks = db.relationship('VendorFeedback', backref='vendor', lazy=True)

    def set_embedding(self, vector):
        self.embedding_json = json.dumps(vector)

    def get_embedding(self):
        return json.loads(self.embedding_json) if self.embedding_json else None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'contact_email': self.contact_email,
            'is_active': self.is_active
        }