import os
import requests
from dotenv import load_dotenv
load_dotenv()

class HuggingFaceClient:
    def __init__(self, api_key: str, model: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"):
        print("DEBUG API KEY:", api_key)  # Tambahkan ini untuk cek
        self.api_key = api_key
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def predict_sentiment(self, text: str):
        payload = {"inputs": text}
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # result: [[{'label': 'POSITIVE', 'score': ...}, ...]]
        # or [{'label': 'POSITIVE', 'score': ...}, ...]
        # Normalize output
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            return result[0]
        return result