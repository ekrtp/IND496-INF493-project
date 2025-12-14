# Rapor gereksinimi: Python 3.10
FROM python:3.10-slim

# Çalışma dizini
WORKDIR /app

# Kütüphaneleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları içeri at
COPY . .

# Uygulamayı başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]