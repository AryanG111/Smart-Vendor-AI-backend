from transformers import pipeline, AutoTokenizer, AutoModel
import torch
import numpy as np

class AIService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIService, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        print("Loading AI Models... This may take a moment.")
        
        # 1. Sentiment Analysis Model (DistilBERT)
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

        # 2. Embedding Model (MiniLM - optimized for sentence similarity)
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.embed_model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        print("AI Models Loaded Successfully.")

    def analyze_sentiment(self, text):
        """Returns: {'label': 'POSITIVE'/'NEGATIVE', 'score': float}"""
        result = self.sentiment_analyzer(text)[0]
        return result

    def generate_embedding(self, text):
        """Returns: List[float] representing the text vector"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.embed_model(**inputs)
        
        # Mean Pooling - Take attention mask into account for correct averaging
        attention_mask = inputs['attention_mask']
        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        embedding = (sum_embeddings / sum_mask).numpy()[0]
        return embedding.tolist()

    def compute_similarity(self, embedding_a, embedding_b):
        """Cosine Similarity"""
        a = np.array(embedding_a)
        b = np.array(embedding_b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Global Instance
ai_service = AIService()