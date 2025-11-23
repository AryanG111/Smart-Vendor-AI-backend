from app.models.feedback import VendorFeedback
from app.extensions import db
from app.services.ai_service import ai_service

class FeedbackService:
    @staticmethod
    def submit_feedback(data):
        # Analyze sentiment
        sentiment_result = ai_service.analyze_sentiment(data['feedback_text'])
        sentiment_label = sentiment_result['label'] # e.g., 'POSITIVE', 'NEGATIVE'
        
        new_feedback = VendorFeedback(
            vendor_id=data['vendor_id'],
            feedback_text=data['feedback_text'],
            sentiment_label=sentiment_label
        )
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback

    @staticmethod
    def get_vendor_feedback(vendor_id):
        return VendorFeedback.query.filter_by(vendor_id=vendor_id).order_by(VendorFeedback.created_at.desc()).all()

    @staticmethod
    def get_vendor_sentiment_score(vendor_id):
        """
        Calculates a sentiment score between 0.0 and 1.0.
        Score = Positive Count / Total Count
        Returns 0.5 (neutral) if no feedback exists.
        """
        feedbacks = VendorFeedback.query.filter_by(vendor_id=vendor_id).all()
        if not feedbacks:
            return 0.5
            
        total = len(feedbacks)
        positive = sum(1 for f in feedbacks if f.sentiment_label == 'POSITIVE')
        
        return positive / total
