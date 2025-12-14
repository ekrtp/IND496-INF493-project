from fastapi import FastAPI
from .schemas import UserRequest, CarResponse
from .recommender import get_hybrid_recommendation
from typing import List

app = FastAPI(title="Araç Öneri Sistemi API")

@app.get("/")
def home():
    return {"message": "API Çalışıyor! Kullanmak için /api/recommend adresine POST isteği atın."}

@app.post("/api/recommend", response_model=List[CarResponse])
def recommend_endpoint(request: UserRequest):
    recommendations = get_hybrid_recommendation(request)
    return recommendations