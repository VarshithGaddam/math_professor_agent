@echo off
echo ========================================
echo Math Professor Agent - Quick Start
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

echo.
echo Checking if virtual environment exists...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Checking .env file...
if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your OpenRouter and Tavily API keys!
    echo Press any key to open .env in notepad...
    pause
    notepad .env
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start Qdrant: docker run -d -p 6333:6333 qdrant/qdrant
echo 2. Initialize KB: python scripts\setup_knowledge_base.py
echo 3. Start backend: uvicorn backend.main:app --reload
echo 4. Start frontend: cd frontend ^&^& npm install ^&^& npm start
echo.
pause
