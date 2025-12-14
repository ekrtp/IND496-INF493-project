@echo off
REM Araç Öneri Sistemi - Hızlı Başlatıcı
REM Bu script hem API'yi hem de Streamlit UI'yi başlatır

echo ========================================
echo    ARAC ONERI SISTEMI BASLATIYOR
echo ========================================
echo.

REM Virtual environment kontrol
if not exist ".venv\Scripts\activate.bat" (
    echo [!] Virtual environment bulunamadi!
    echo [*] Olusturuluyor...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo [*] Virtual environment aktive edildi
echo.

REM İki ayrı terminal açmak için start komutunu kullan
echo [*] Backend API baslatilayor...
start "Arac Oneri API" cmd /k "cd /d %CD% && .venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo [*] Streamlit UI baslatilayor...
start "Arac Oneri UI" cmd /k "cd /d %CD% && .venv\Scripts\activate.bat && streamlit run streamlit_app.py"

echo.
echo ========================================
echo    SISTEM BASLATILDI!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Streamlit UI: http://localhost:8501
echo.
echo Kapatmak icin her iki terminal penceresini kapatin
echo.
pause
