import pytest
import json
import os
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models.vendor import Vendor

# Mock Config for Testing
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = 'test-key'

@pytest.fixture
def client():
    # Patch the AI Service to avoid loading heavy models
    with patch('app.services.ai_service.ai_service') as mock_ai:
        # Mock embedding generation
        mock_ai.generate_embedding.return_value = [0.1, 0.2, 0.3]
        # Mock similarity computation
        mock_ai.compute_similarity.return_value = 0.9
        
        os.environ['API_KEY'] = 'test-key'
        app = create_app(TestConfig)
        
        # Create tables
        with app.app_context():
            db.create_all()
            yield app.test_client()
            db.session.remove()
            db.drop_all()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_vendor(client):
    headers = {'X-API-KEY': 'test-key'}
    data = {
        "name": "Tech Solutions Inc.",
        "category": "IT Services",
        "description": "Provider of cloud solutions and software development.",
        "contact_email": "contact@techsolutions.com"
    }
    
    response = client.post('/vendors', json=data, headers=headers)
    assert response.status_code == 201
    assert response.json['message'] == "Vendor created"
    
    # Verify DB
    with client.application.app_context():
        vendor = Vendor.query.first()
        assert vendor is not None
        assert vendor.name == "Tech Solutions Inc."
        assert vendor.get_embedding() == [0.1, 0.2, 0.3]

def test_recommend_vendors(client):
    headers = {'X-API-KEY': 'test-key'}
    
    # 1. Create a vendor first
    client.post('/vendors', json={
        "name": "Tech Solutions Inc.",
        "category": "IT Services",
        "description": "Cloud stuff",
        "contact_email": "contact@techsolutions.com"
    }, headers=headers)
    
    # 2. Request recommendation
    req_data = {
        "description": "Looking for cloud providers",
        "category": "IT Services"
    }
    
    response = client.post('/vendors/recommend', json=req_data, headers=headers)
    assert response.status_code == 200
    results = response.json
    assert isinstance(results, list)
    assert len(results) > 0
    assert results[0]['vendor_name'] == "Tech Solutions Inc."
