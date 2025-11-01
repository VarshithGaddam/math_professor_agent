#!/bin/bash

echo "========================================"
echo "Math Professor Agent - Quick Start"
echo "========================================"
echo ""

echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python not found. Please install Python 3.11+"
    exit 1
fi

echo ""
echo "Checking if virtual environment exists..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Checking .env file..."
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env and add your OpenRouter and Tavily API keys!"
    echo "Opening .env in default editor..."
    ${EDITOR:-nano} .env
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Start Qdrant: docker run -d -p 6333:6333 qdrant/qdrant"
echo "2. Initialize KB: python scripts/setup_knowledge_base.py"
echo "3. Start backend: uvicorn backend.main:app --reload"
echo "4. Start frontend: cd frontend && npm install && npm start"
echo ""
