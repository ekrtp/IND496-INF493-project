import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Modeli global olarak bir kere yüklüyoruz
model = SentenceTransformer('all-MiniLM-L6-v2')

# Docker içindeki yol veya local yol
CSV_PATH = "/app/data/used_cars.csv"
if not os.path.exists(CSV_PATH):
    # Eğer Docker değilse, local path kullan
    CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "used_cars.csv")
    CSV_PATH = os.path.normpath(CSV_PATH)

def load_data():
    """CSV dosyasını yükler ve temizler"""
    if not os.path.exists(CSV_PATH):
        print(f"UYARI: Veri dosyası bulunamadı: {CSV_PATH}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(CSV_PATH)
        # Fiyat sütunundaki $ ve , işaretlerini temizleyip sayıya çevirelim (Güvenlik önlemi)
        # Eğer veri zaten temizse bu adım hata vermez, try-except içinde kalsın.
        if df['price'].dtype == 'O': # Object (String) ise
            df['price'] = df['price'].astype(str).str.replace('$', '').str.replace(',', '').astype(float)
        return df
    except Exception as e:
        print(f"Veri yükleme hatası: {e}")
        return pd.DataFrame()

# Veriyi belleğe al
global_df = load_data()

def get_hybrid_recommendation(user_req):
    global global_df
    
    if global_df.empty:
        # Veri yüklenmemişse tekrar dene (belki dosya sonradan gelmiştir)
        global_df = load_data()
        if global_df.empty:
            return []

    # 1. ADIM: PANDAS FİLTRELEME (Hard Filter)
    # Fiyat ve Yıl kriterlerine göre eleme
    filtered_df = global_df[
        (global_df['price'] <= user_req.max_price) & 
        (global_df['price'] >= user_req.min_price) & 
        (global_df['model_year'] >= user_req.min_year)
    ].copy()

    if filtered_df.empty:
        return []

    # 2. ADIM: AI İLE ANLAMSAL ARAMA (Soft Filter)
    # Araç özelliklerini tek bir metinde birleştir
    # CSV Sütunları: brand, model, transmission, engine, fuel_type, ext_col
    # NaN değerleri boş string ile değiştir
    text_columns = ['brand', 'model', 'transmission', 'engine', 'fuel_type', 'ext_col']
    for col in text_columns:
        filtered_df[col] = filtered_df[col].fillna('').astype(str)
    
    filtered_df['text_repr'] = (
        filtered_df['brand'] + " " + 
        filtered_df['model'] + " " + 
        filtered_df['transmission'] + " " + 
        filtered_df['engine'] + " " +
        filtered_df['fuel_type'] + " color: " +
        filtered_df['ext_col']
    )
    
    # Vektörleştirme
    car_vectors = model.encode(filtered_df['text_repr'].tolist())
    user_vector = model.encode([user_req.query_text])
    
    # Benzerlik Hesaplama
    scores = cosine_similarity(user_vector, car_vectors)[0]
    filtered_df['similarity_score'] = scores
    
    # En iyi 5 sonucu seç
    results = filtered_df.sort_values(by='similarity_score', ascending=False).head(5)
    
    response_list = []
    for _, row in results.iterrows():
        response_list.append({
            "brand": row['brand'],
            "model": row['model'],
            "model_year": int(row['model_year']),
            "price": float(row['price']),
            "milage": str(row['milage']),
            "fuel_type": str(row['fuel_type']),
            "transmission": str(row['transmission']),
            "similarity_score": float(row['similarity_score']),
            "reason": f"Sorgunuzla %{int(row['similarity_score']*100)} oranında eşleşiyor."
        })
        
    return response_list