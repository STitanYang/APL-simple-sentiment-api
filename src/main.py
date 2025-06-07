from fastapi import FastAPI
from src.api.v1.sentiment import router as sentiment_router

app = FastAPI()

app.include_router(sentiment_router, prefix="/api/v1", tags=["sentiment"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentiment Analysis API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)