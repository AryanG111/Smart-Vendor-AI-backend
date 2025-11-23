from app.models.purchase_request import PurchaseRequest
from app.extensions import db

class PurchaseService:
    @staticmethod
    def create_request(data):
        new_req = PurchaseRequest(
            category=data['category'],
            description=data['description'],
            urgency=data['urgency'],
            budget=data['budget']
        )
        db.session.add(new_req)
        db.session.commit()
        return new_req

    @staticmethod
    def get_all_requests():
        return PurchaseRequest.query.order_by(PurchaseRequest.created_at.desc()).all()

    @staticmethod
    def get_request_by_id(req_id):
        return PurchaseRequest.query.get(req_id)
