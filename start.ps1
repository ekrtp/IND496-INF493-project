# Araç Öneri Sistemi - Hızlı Başlatıcı (PowerShell)
# Bu script hem API'yi hem de Streamlit UI'yi başlatır

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ARAÇ ÖNERİ SİSTEMİ BAŞLATIYOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Virtual environment kontrol
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "[!] Virtual environment bulunamadı!" -ForegroundColor Yellow
    Write-Host "[*] Oluşturuluyor..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
} else {
    & .\.venv\Scripts\Activate.ps1
}

Write-Host "[*] Virtual environment aktive edildi" -ForegroundColor Green
Write-Host ""

# Backend API'yi başlat (yeni terminal)
Write-Host "[*] Backend API başlatılıyor..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 3

# Streamlit UI'yi başlat (yeni terminal)
Write-Host "[*] Streamlit UI başlatılıyor..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; streamlit run streamlit_app.py"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   SİSTEM BAŞLATILDI!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API: " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host "Streamlit UI: " -NoNewline; Write-Host "http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Kapatmak için her iki terminal penceresini kapatın" -ForegroundColor Yellow
Write-Host ""
