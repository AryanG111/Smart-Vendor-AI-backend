# SmartVendor AI — Backend

A complete backend application for enterprises to manage vendors, track performance, analyze feedback using AI, and receive intelligent vendor recommendations.

## Tech Stack
- **Language**: Python
- **Framework**: Flask
- **Database**: Microsoft SQL Server (MSSQL)
- **ORM**: SQLAlchemy
- **AI/ML**: HuggingFace Transformers (DistilBERT, MiniLM)

## Features
1. **Vendor Management**: CRUD operations for vendors.
2. **Performance Tracking**: Track monthly performance metrics (Quality, Timeliness, Cost).
3. **Purchase Requests**: Create and manage purchase requests.
4. **Feedback & Sentiment Analysis**: Analyze vendor feedback using AI.
5. **Vendor Recommendations**: Intelligent recommendations based on text similarity, category, and performance.
6. **Security**: API Key-based authentication.
7. **Logging**: Comprehensive request/response logging.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Microsoft SQL Server (Local or Remote)
- ODBC Driver 17 for SQL Server

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Environment Variables:
   - Create a `.env` file (or use system env vars):
     ```
     DB_SERVER=localhost
     DB_NAME=SmartVendorDB
     API_KEY=your-secret-key
     ```

### Running the Application
```bash
python run.py
```
The server will start at `http://127.0.0.1:5000`.

## API Endpoints

**Authentication**: All endpoints (except `/health`, `/readiness`) require header `X-API-KEY: <your-key>`.

### Vendor Management
- `POST /vendors`: Create a new vendor.
- `GET /vendors`: List all vendors (params: `category`, `active_only`).
- `GET /vendors/<id>`: Get vendor details.
- `PUT /vendors/<id>`: Update vendor details.
- `DELETE /vendors/<id>`: Delete a vendor.

### Performance
- `POST /performance`: Add performance record.
- `GET /vendors/<id>/performance`: Get performance history.
- `GET /performance/top`: Get top performing vendors.

### Purchase Requests
- `POST /purchase-requests`: Create a purchase request.
- `GET /purchase-requests`: List all requests.
- `GET /purchase-requests/<id>`: Get request details.

### Feedback
- `POST /feedback`: Submit feedback (auto-analyzed for sentiment).
- `GET /vendors/<id>/feedback`: Get vendor feedback.

### Recommendations
- `POST /vendors/recommend`: Get vendor recommendations for a purchase request.

### System
- `GET /health`: Health check.
- `GET /readiness`: Database connection check.

## AI Models
- **Sentiment Analysis**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
