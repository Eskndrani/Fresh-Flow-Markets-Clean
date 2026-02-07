@echo off
echo.
echo ========================================
echo   Fresh Flow Markets - Starting...
echo ========================================
echo.
echo [1/3] Starting API Server...
start /min powershell -NoExit -Command "python app.py"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Dashboard...
start /min powershell -NoExit -Command "streamlit run dashboard.py"
timeout /t 3 /nobreak >nul

echo [3/3] Opening Website Demo...
code website_integration_demo.html

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo API:       http://localhost:5000
echo Dashboard: http://localhost:8501
echo Website:   Opened in VS Code
echo.
