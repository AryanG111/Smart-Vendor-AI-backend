from app import create_app, db
from app.services.ai_service import ai_service

app = create_app()

# Create tables before running
with app.app_context():
    try:
        print("Checking database tables...")
        db.create_all()
        print("Database tables created/verified successfully.")
        
        # Pre-load AI models to ensure readiness
        _ = ai_service 
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    # Run on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)