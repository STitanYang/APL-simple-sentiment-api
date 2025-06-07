from pydantic import BaseModel

class SentimentResult(BaseModel):
    label: str
    score: float

class SentimentRequest(BaseModel):
    text: str