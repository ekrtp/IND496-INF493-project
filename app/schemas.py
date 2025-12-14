from pydantic import BaseModel
from typing import Optional

# Kullanıcıdan gelen istek
class UserRequest(BaseModel):
    query_text: str  # Örn: "Az yakan şehir içi araç"
    min_price: int = 0
    max_price: int = 5000000
    min_year: Optional[int] = 2010

# Kullanıcıya dönecek cevap (CSV sütunlarına uyumlu)
class CarResponse(BaseModel):
    brand: str
    model: str
    model_year: int
    price: float  # CSV'de sayısal olduğunu varsayıyoruz
    milage: str   # CSV'de "120,000 mi" gibi string olabilir
    fuel_type: str
    transmission: str
    similarity_score: float
    reason: str