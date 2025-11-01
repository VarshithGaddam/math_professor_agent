@echo off
echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements...
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install pydantic==2.4.2
pip install python-multipart==0.0.6
pip install langgraph==0.0.20
pip install langchain==0.1.4
pip install langchain-openai==0.0.5
pip install langchain-community==0.0.16
pip install qdrant-client==1.7.0
pip install sentence-transformers==2.2.2
pip install openai==1.6.1
pip install httpx==0.25.2
pip install dspy-ai==2.4.0
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install pyarrow==12.0.1
pip install python-dotenv==1.0.0
pip install pyyaml==6.0.1
pip install loguru==0.7.2

echo Installation complete!
pause