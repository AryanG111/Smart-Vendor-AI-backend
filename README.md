# Smart Vendor AI Backend

A Flask-based backend application for an AI-powered vendor recommendation system. This system uses machine learning embeddings to match vendor capabilities with purchase requirements.

## Features

*   **Vendor Management**: Create and store vendor profiles with detailed descriptions.
*   **AI-Powered Recommendations**: Uses text embeddings (via Transformers) to semantically match purchase descriptions with suitable vendors.
*   **Performance Tracking**: Track vendor performance metrics like delivery time and quality.
*   **Feedback System**: Collect and store user feedback.
*   **Secure API**: API key authentication for endpoints.

## Tech Stack

*   **Framework**: Flask
*   **Database**: SQL Server (via PyODBC), SQLAlchemy ORM
*   **AI/ML**: Hugging Face Transformers, PyTorch, Scikit-learn
*   **Utilities**: Python-dotenv, NumPy

## Prerequisites

*   Python 3.8+
*   SQL Server (or compatible database configured in connection string)

## Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd "Smart Vendor"
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add the following variables (adjust as needed):
    ```env
    DATABASE_URL=mssql+pyodbc://<username>:<password>@<server>/<database>?driver=ODBC+Driver+17+for+SQL+Server
    API_KEY=your_secret_api_key
    ```

## Running the Application

To start the Flask development server:

```bash
python run.py
```

The server will start on `http://0.0.0.0:5000`.

## API Endpoints

### 1. Create Vendor
**POST** `/vendors`
*   **Headers**: `x-api-key: <your_api_key>`
*   **Body**:
    ```json
    {
        "name": "Vendor Name",
        "category": "Electronics",
        "description": "Supplier of high quality electronic components...",
        "contact_email": "contact@vendor.com"
    }
    ```

### 2. Recommend Vendors
**POST** `/vendors/recommend`
*   **Headers**: `x-api-key: <your_api_key>`
*   **Body**:
    ```json
    {
        "category": "Electronics",
        "description": "Looking for bulk resistors and capacitors"
    }
    ```

## Project Structure

```text
Smart Vendor/
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── app/                        # Main application package
    ├── __init__.py             # App factory
    ├── config.py               # Configuration
    ├── extensions.py           # Flask extensions
    ├── models/                 # Database models
    ├── routes/                 # API routes
    ├── services/               # Business logic (AI, Recommendations)
    └── utils/                  # Utilities (Auth)
```
