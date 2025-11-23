from app.models.vendor import Vendor
from app.extensions import db
from app.services.ai_service import ai_service

class VendorService:
    @staticmethod
    def create_vendor(data):
        # Generate embedding
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
        return new_vendor

    @staticmethod
    def get_all_vendors(category=None, active_only=False):
        query = Vendor.query
        if category:
            query = query.filter(Vendor.category == category)
        if active_only:
            query = query.filter(Vendor.is_active == True)
        return query.all()

    @staticmethod
    def get_vendor_by_id(vendor_id):
        return Vendor.query.get(vendor_id)

    @staticmethod
    def update_vendor(vendor_id, data):
        vendor = Vendor.query.get(vendor_id)
        if not vendor:
            return None
        
        if 'name' in data: vendor.name = data['name']
        if 'category' in data: vendor.category = data['category']
        if 'description' in data: vendor.description = data['description']
        if 'contact_email' in data: vendor.contact_email = data['contact_email']
        if 'is_active' in data: vendor.is_active = data['is_active']
        
        # Regenerate embedding if category or description changes
        if 'category' in data or 'description' in data:
            embedding = ai_service.generate_embedding(f"{vendor.category} {vendor.description}")
            vendor.set_embedding(embedding)
            
        db.session.commit()
        return vendor

    @staticmethod
    def delete_vendor(vendor_id):
        vendor = Vendor.query.get(vendor_id)
        if not vendor:
            return False
            
        # Manually delete related records to avoid IntegrityError
        # 1. Delete Performance records
        for perf in vendor.performances:
            db.session.delete(perf)
            
        # 2. Delete Feedback records
        for feedback in vendor.feedbacks:
            db.session.delete(feedback)
            
        # 3. Delete the Vendor
        db.session.delete(vendor)
        db.session.commit()
        return True

