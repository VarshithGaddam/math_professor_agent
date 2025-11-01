@echo off
echo ========================================
echo Step-by-Step Installation for Python 3.9
echo ========================================

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo Step 2: Installing core packages...
pip install fastapi uvicorn pydantic python-multipart
if errorlevel 1 (
    echo ERROR: Failed to install core packages
    pause
    exit /b 1
)

echo Step 3: Installing OpenAI (latest version)...
pip install "openai>=1.10.0"
if errorlevel 1 (
    echo ERROR: Failed to install OpenAI
    pause
    exit /b 1
)

echo Step 4: Installing LangChain packages...
pip install langchain langchain-openai langchain-community
if errorlevel 1 (
    echo ERROR: Failed to install LangChain
    pause
    exit /b 1
)

echo Step 5: Installing LangGraph...
pip install langgraph
if errorlevel 1 (
    echo ERROR: Failed to install LangGraph
    pause
    exit /b 1
)

echo Step 6: Installing vector database...
pip install qdrant-client sentence-transformers
if errorlevel 1 (
    echo ERROR: Failed to install vector packages
    pause
    exit /b 1
)

echo Step 7: Installing utilities...
pip install httpx python-dotenv pyyaml loguru numpy pandas
if errorlevel 1 (
    echo ERROR: Failed to install utilities
    pause
    exit /b 1
)

echo Step 8: Installing DSPy (optional)...
pip install dspy-ai
if errorlevel 1 (
    echo WARNING: DSPy installation failed, continuing without it...
)

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Test API: python scripts\test_openrouter.py
echo 2. Start Qdrant: docker run -d -p 6333:6333 qdrant/qdrant
echo 3. Setup KB: python scripts\setup_knowledge_base.py
echo.
pause