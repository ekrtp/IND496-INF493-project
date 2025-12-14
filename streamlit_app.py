import streamlit as st
import requests
import json
from typing import List, Dict

# Sayfa yapılandırması
st.set_page_config(
    page_title="🚗 Araç Öneri Asistanı",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .car-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .car-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .car-detail {
        font-size: 14px;
        margin: 5px 0;
        opacity: 0.9;
    }
    .price-tag {
        font-size: 28px;
        font-weight: bold;
        color: #FFD700;
        margin: 10px 0;
    }
    .similarity-badge {
        background-color: rgba(255,255,255,0.3);
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 10px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: fadeIn 0.5s;
        color: #000;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 30px;
        border-radius: 25px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = "http://localhost:8000/api/recommend"

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_recommendations' not in st.session_state:
    st.session_state.last_recommendations = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

def format_price(price: float) -> str:
    """Fiyatı güzel formatta göster"""
    return f"${price:,.0f}"

def display_car_card(car: Dict, index: int):
    """Araç kartını görsel olarak göster"""
    similarity_percent = int(car['similarity_score'] * 100)
    
    # Renk gradyanları
    gradients = [
        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
    ]
    
    gradient = gradients[index % len(gradients)]
    
    st.markdown(f"""
    <div style="background: {gradient}; padding: 20px; border-radius: 15px; margin: 10px 0; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">
            {car['brand']} {car['model']}
        </div>
        <div style="font-size: 28px; font-weight: bold; color: #FFD700; margin: 10px 0;">
            {format_price(car['price'])}
        </div>
        <div style="font-size: 14px; margin: 5px 0; opacity: 0.9;">
            📅 Yıl: {car['model_year']} | 🛣️ KM: {car['milage']}
        </div>
        <div style="font-size: 14px; margin: 5px 0; opacity: 0.9;">
            ⛽ Yakıt: {car['fuel_type']} | ⚙️ Vites: {car['transmission']}
        </div>
        <div style="background-color: rgba(255,255,255,0.3); padding: 5px 15px; border-radius: 20px; display: inline-block; margin-top: 10px;">
            🎯 Eşleşme: %{similarity_percent}
        </div>
        <div style="font-size: 13px; margin-top: 10px; font-style: italic;">
            💬 {car['reason']}
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_recommendations(query: str, min_price: int, max_price: int, min_year: int) -> List[Dict]:
    """API'den öneri al"""
    try:
        payload = {
            "query_text": query,
            "min_price": min_price,
            "max_price": max_price,
            "min_year": min_year
        }
        
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API hatası: {str(e)}")
        return []

# Ana başlık
st.title("🚗 Araç Öneri Asistanı")
st.markdown("### AI destekli akıllı araç arama sistemi")

# Sidebar - Filtreler
with st.sidebar:
    st.header("🔍 Arama Filtreleri")
    
    min_price = st.number_input(
        "💰 Minimum Fiyat ($)",
        min_value=0,
        max_value=1000000,
        value=0,
        step=1000,
        help="Aradığınız aracın minimum fiyatı"
    )
    
    max_price = st.number_input(
        "💰 Maximum Fiyat ($)",
        min_value=0,
        max_value=5000000,
        value=100000,
        step=1000,
        help="Aradığınız aracın maksimum fiyatı"
    )
    
    min_year = st.number_input(
        "📅 Minimum Model Yılı",
        min_value=1990,
        max_value=2025,
        value=2010,
        step=1,
        help="Aradığınız aracın en eski model yılı"
    )
    
    st.markdown("---")
    st.markdown("### 💡 Örnek Aramalar")
    example_queries = [
        "Az yakan şehir içi araç",
        "Ailem için geniş SUV",
        "Spor araba performanslı",
        "Ekonomik hibrit araç",
        "Lüks sedan yüksek performans",
        "Öğrenciye uygun, bütçe dostu",
        "Şehir içi kompakt, parkı kolay",
        "Uzun yolda konforlu ve güvenli",
        "Düşük kilometreli, temiz title",
        "Elektrikli veya plug-in hibrit"
    ]
    
    for query in example_queries:
        if st.button(query, key=f"example_{query}", width='stretch'):
            st.session_state.user_input = query

# Ana bölüm - İki kolon
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💬 Sohbet Asistanı")
    
    # Kullanıcı girişi
    user_input = st.text_area(
        "Nasıl bir araç arıyorsunuz?",
        height=100,
        placeholder="Örnek: Ailem için güvenli ve geniş bir SUV arıyorum...",
        help="Aradığınız aracı detaylı şekilde anlatın",
        key="user_input"
    )
    
    search_button = st.button("🔍 Araç Öner", width='stretch', type="primary")
    should_run = search_button
    
    # Arama yap
    if should_run and st.session_state.user_input:
        with st.spinner("🤖 AI araçları analiz ediyor..."):
            recommendations = get_recommendations(st.session_state.user_input, min_price, max_price, min_year)
            
            # Chat history'ye ekle
            st.session_state.chat_history.append({
                "role": "user",
                "content": st.session_state.user_input
            })
            
            if recommendations:
                st.session_state.last_recommendations = recommendations
                response_text = f"✅ Kriterlerinize uygun {len(recommendations)} araç buldum!"
            else:
                st.session_state.last_recommendations = []
                response_text = "😕 Üzgünüm, kriterlerinize uygun araç bulunamadı. Filtreleri genişletmeyi deneyin."
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_text
            })
    
    # Chat history göster
    st.markdown("---")
    st.markdown("#### 📜 Konuşma Geçmişi")
    
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 Siz:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Asistan:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🗑️ Geçmişi Temizle", width='stretch'):
            st.session_state.chat_history = []
            st.session_state.last_recommendations = []
            st.rerun()
    else:
        st.info("💭 Henüz arama yapılmadı. Yukarıdan bir arama yaparak başlayın!")

with col2:
    st.subheader("🎯 Önerilen Araçlar")
    
    if st.session_state.last_recommendations:
        # Tabs ile farklı görünümler
        tab1, tab2 = st.tabs(["📊 Kart Görünümü", "📋 Liste Görünümü"])
        
        with tab1:
            for idx, car in enumerate(st.session_state.last_recommendations):
                display_car_card(car, idx)
        
        with tab2:
            # Tablo görünümü
            import pandas as pd
            df_display = pd.DataFrame(st.session_state.last_recommendations)
            df_display['price'] = df_display['price'].apply(format_price)
            df_display['similarity_score'] = df_display['similarity_score'].apply(lambda x: f"%{int(x*100)}")
            
            # Sadece önemli sütunları göster
            columns_to_show = ['brand', 'model', 'model_year', 'price', 'fuel_type', 'similarity_score']
            df_display = df_display[columns_to_show]
            df_display.columns = ['Marka', 'Model', 'Yıl', 'Fiyat', 'Yakıt', 'Eşleşme']
            
            st.dataframe(df_display, width='stretch', hide_index=True)
        
        # İstatistikler
        st.markdown("---")
        st.markdown("#### 📊 Özet İstatistikler")
        
        prices = [car['price'] for car in st.session_state.last_recommendations]
        years = [car['model_year'] for car in st.session_state.last_recommendations]
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("💰 Ortalama Fiyat", format_price(sum(prices) / len(prices)))
        
        with stat_col2:
            st.metric("📅 Ortalama Yıl", f"{int(sum(years) / len(years))}")
        
        with stat_col3:
            avg_similarity = sum(car['similarity_score'] for car in st.session_state.last_recommendations) / len(st.session_state.last_recommendations)
            st.metric("🎯 Ort. Eşleşme", f"%{int(avg_similarity * 100)}")
        
    else:
        st.info("🔍 Araç öneri almak için sol taraftan arama yapın!")
        
        # Placeholder görseli
        st.markdown("""
        <div style="text-align: center; padding: 50px; opacity: 0.5;">
            <div style="font-size: 80px;">🚗</div>
            <div style="font-size: 20px; margin-top: 20px;">
                Hayalinizdeki aracı bulmak için aramaya başlayın!
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; opacity: 0.7; padding: 20px;">
    🤖 AI Destekli Araç Öneri Sistemi | Powered by Sentence Transformers & FastAPI<br>
    Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
