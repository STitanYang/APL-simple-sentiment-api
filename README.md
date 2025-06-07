# Sentiment Analysis API

This project is a FastAPI application that provides a RESTful API for sentiment analysis. It allows users to submit text, such as product reviews or social media comments, and receive feedback on whether the sentiment of the text is positive or negative. The sentiment analysis is powered by the Hugging Face Inference API using the DistilBERT model (`distilbert-base-uncased-finetuned-sst-2-english`).

## Project Structure

```
sentiment-api
├── src
│   ├── main.py                # Entry point for the FastAPI application
│   ├── api
│   │   └── v1
│   │       └── sentiment.py   # API endpoints for sentiment analysis
│   ├── services
│   │   └── huggingface_client.py # Handles communication with Hugging Face API
│   ├── models
│   │   └── sentiment.py       # Data models for sentiment analysis results
│   ├── schemas
│   │   └── sentiment.py       # Pydantic schemas for request and response validation
│   └── utils
│       └── __init__.py       # Utility functions and classes
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .env                       # Environment variables
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sentiment-api.git
   cd sentiment-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Hugging Face API key:
   ```
   HUGGINGFACE_API_KEY=your_api_key_here
   MODEL_NAME=your_model_name
   DATABASE_URL=your_database_url
   ```

## Usage

To run the FastAPI application, execute the following command:
```
uvicorn src.main:app --reload
```

You can access the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### POST /api/v1/analyze

- **Request Body**: 
  ```json
  {
    "text": "Your text here"
  }
  ```

- **Response**:
  ```json
  {
    "sentiment": "positive" or "negative",
    "score": 0.95
  }
  ```

### GET /api/v1/requests

- **Response**:
  ```json
  [
    {
        "id": 4,
        "user_id": 1,
        "comment_text": "Produk ini cukup mengecewakan!",
        "created_date": "2025-06-06"
    },
    {
        "id": 5,
        "user_id": 1,
        "comment_text": "Produk ini bagus!",
        "created_date": "2025-06-06"
    },
    ...
   ]
  ```

### GET /api/v1/requests/{id}

- **Response**:
  ```json
  {
    "id": 5,
    "user_id": 1,
    "comment_text": "Produk ini bagus!",
    "created_date": "2025-06-06",
    "result": {
        "label": "positive",
        "score": 0.966884195804596,
        "processed_time": "2025-06-06T13:06:55.297706"
    }
   }
  ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
