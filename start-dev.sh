#!/usr/bin/env bash
# AgentForge AI – Development Start Script

set -e

echo "🚀 Starting AgentForge AI..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[1/3] Starting Backend...${NC}"
if [ ! -f ".venv/bin/activate" ] && [ ! -f ".venv/Scripts/activate" ]; then
  python -m venv .venv
fi

# Activate venv
if [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate  # Windows
else
  source .venv/bin/activate       # Unix
fi

cd backend
pip install -r requirements.txt -q
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend running at http://localhost:8000${NC}"
cd ..

echo ""
echo -e "${BLUE}[2/3] Starting Frontend...${NC}"
cd frontend
npm install -q
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend running at http://localhost:5173${NC}"
cd ..

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  AgentForge AI is running!             ${NC}"
echo -e "${GREEN}  Frontend: http://localhost:5173        ${NC}"
echo -e "${GREEN}  Backend:  http://localhost:8000        ${NC}"
echo -e "${GREEN}  API Docs: http://localhost:8000/docs   ${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
