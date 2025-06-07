from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from datetime import date, datetime
from src.schemas.sentiment import SentimentRequest, SentimentResponse
from src.services.huggingface_client import HuggingFaceClient
from src.db.session import SessionLocal
from src.models.db_models import Request, Result, User

import os

router = APIRouter()
client = HuggingFaceClient(
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. POST /api/analyze
@router.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(
    request: SentimentRequest,
    db: Session = Depends(get_db)
):
    try:
        # Pastikan user dengan id=1 ada
        user = db.query(User).filter_by(id=1).first()
        if not user:
            raise HTTPException(status_code=400, detail="User default belum diinisialisasi.")
        results = client.predict_sentiment(request.text)
        if isinstance(results, list) and results:
            top_result = max(results, key=lambda x: x["score"])
            # Simpan ke tabel requests
            req = Request(
                user_id=1,
                comment_text=request.text,
                created_date=date.today()
            )
            db.add(req)
            db.commit()
            db.refresh(req)
            # Simpan ke tabel results
            res = Result(
                requests_id=req.id,
                label=top_result["label"].lower(),
                score=top_result["score"],
                processed_time=datetime.now()
            )
            db.add(res)
            db.commit()
            return SentimentResponse(
                sentiment=top_result["label"].lower(),
                score=top_result["score"]
            )
        raise HTTPException(status_code=500, detail="Invalid response from HuggingFace API")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 2. GET /api/requests
@router.get("/requests")
def get_all_requests(db: Session = Depends(get_db)):
    requests = db.query(Request).all()
    result = []
    for req in requests:
        result.append({
            "id": req.id,
            "user_id": req.user_id,
            "comment_text": req.comment_text,
            "created_date": req.created_date
        })
    return result

# 3. GET /api/requests/{id}
@router.get("/requests/{request_id}")
def get_request_detail(
    request_id: int = Path(..., description="ID request"),
    db: Session = Depends(get_db)
):
    req = db.query(Request).filter_by(id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")
    res = db.query(Result).filter_by(requests_id=req.id).first()
    return {
        "id": req.id,
        "user_id": req.user_id,
        "comment_text": req.comment_text,
        "created_date": req.created_date,
        "result": {
            "label": res.label if res else None,
            "score": res.score if res else None,
            "processed_time": res.processed_time if res else None
        }
    }