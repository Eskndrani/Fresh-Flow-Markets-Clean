# Fresh Flow Markets - Startup Script
# Starts API, Dashboard, and opens website demo

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fresh Flow Markets - Starting..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Start Flask API
Write-Host "[1/3] Starting API Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python app.py" -WindowStyle Minimized
Start-Sleep 3

# Start Streamlit Dashboard
Write-Host "[2/3] Starting Dashboard..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; streamlit run dashboard.py" -WindowStyle Minimized
Start-Sleep 3

# Open website demo in VS Code
Write-Host "[3/3] Opening Website Demo..." -ForegroundColor Yellow
code website_integration_demo.html

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  All Services Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nAPI:       http://localhost:5000" -ForegroundColor White
Write-Host "Dashboard: http://localhost:8501" -ForegroundColor White
Write-Host "Website:   Opened in VS Code" -ForegroundColor White
Write-Host "`nPress Ctrl+C to stop this script" -ForegroundColor Gray
Write-Host "(API and Dashboard will continue running in background)`n" -ForegroundColor Gray

# Keep script running
while ($true) { Start-Sleep 1 }
