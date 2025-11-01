@echo off
echo Restarting Math Professor Agent Backend...
echo.

echo Stopping any existing server...
taskkill /f /im python.exe 2>nul

echo.
echo Starting backend server...
uvicorn backend.main:app --reload --port 8000

pause