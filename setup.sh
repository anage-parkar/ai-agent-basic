#!/bin/bash

# DataPilot Setup Script
# This script helps you set up the DataPilot agent quickly

set -e

echo "🤖 DataPilot Setup Script"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running from correct directory
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: Please run this script from the ai-agent-starter directory"
    exit 1
fi

# Backend setup
echo "📦 Setting up Backend..."
cd backend

if [ ! -f ".env" ]; then
    echo "  Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}  ⚠️  Please edit backend/.env with your API keys${NC}"
else
    echo "  .env already exists, skipping..."
fi

echo "  Installing Python dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}  ✓ Backend setup complete${NC}"
echo ""

# Frontend setup
echo "📦 Setting up Frontend..."
cd ../frontend

if [ ! -f ".env" ]; then
    echo "  Creating .env from .env.example..."
    cp .env.example .env
else
    echo "  .env already exists, skipping..."
fi

echo "  Installing Node dependencies..."
npm install

echo -e "${GREEN}  ✓ Frontend setup complete${NC}"
echo ""

cd ..

# Summary
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your API keys:"
echo "   ${YELLOW}Edit backend/.env with your LLM provider credentials${NC}"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   uvicorn app:app --reload --port 8000"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser to:"
echo "   ${GREEN}http://localhost:5173${NC}"
echo ""
echo "📚 See README.md for detailed documentation"
echo ""
