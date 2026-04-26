#!/bin/bash

# HealthAI - Start Backend & Frontend
# This script starts both the Flask backend and Next.js frontend servers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║     🌿 Starting HealthAI Backend & Frontend 🌿       ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get the root directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Check if directories exist
if [ ! -d "$BACKEND_DIR" ]; then
  echo -e "${RED}✗ Backend directory not found at $BACKEND_DIR${NC}"
  exit 1
fi

if [ ! -d "$FRONTEND_DIR" ]; then
  echo -e "${RED}✗ Frontend directory not found at $FRONTEND_DIR${NC}"
  exit 1
fi

# Create logs directory
LOGS_DIR="$ROOT_DIR/logs"
mkdir -p "$LOGS_DIR"

# Function to cleanup on exit
cleanup() {
  echo -e "\n${YELLOW}Stopping servers...${NC}"
  kill $BACKEND_PID 2>/dev/null || true
  kill $FRONTEND_PID 2>/dev/null || true
  echo -e "${GREEN}✓ Servers stopped${NC}"
}

trap cleanup EXIT

# Start Backend
echo -e "${BLUE}▶ Starting Backend Server (with auto-reload)...${NC}"
cd "$BACKEND_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo -e "${YELLOW}Creating virtual environment...${NC}"
  python -m venv venv
fi

# Activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
  # Windows bash (Git Bash / MSYS2)
  source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
  # Unix-like
  source venv/bin/activate
fi

# Install/update requirements
if [ -f "requirements.txt" ]; then
  echo -e "${YELLOW}Installing backend dependencies...${NC}"
  pip install -q -r requirements.txt 2>/dev/null || echo -e "${YELLOW}⚠ Some dependencies may not have installed${NC}"
fi

# Start backend server
python run.py > "$LOGS_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo -e "${GREEN}  🔗 API: http://localhost:5000${NC}"
echo -e "${YELLOW}  💡 Restart backend manually to reload code${NC}"

# Start Frontend
echo -e "${BLUE}▶ Starting Frontend Server...${NC}"
cd "$FRONTEND_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
  echo -e "${YELLOW}Installing frontend dependencies...${NC}"
  npm install --legacy-peer-deps 2>/dev/null || npm install 2>/dev/null || echo -e "${YELLOW}⚠ npm install had issues${NC}"
fi

# Start frontend dev server
npm run dev > "$LOGS_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo -e "${GREEN}  🔗 App: http://localhost:3000${NC}"

# Wait for both servers to start
sleep 2

# Display status
echo -e "\n${BLUE}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│${NC}  ${GREEN}✓ Both servers are running!${NC}${BLUE}                       │${NC}"
echo -e "${BLUE}├─────────────────────────────────────────────────────┤${NC}"
echo -e "${BLUE}│${NC}  Frontend:  ${GREEN}http://localhost:3000${NC}${BLUE}              │${NC}"
echo -e "${BLUE}│${NC}  Backend:   ${GREEN}http://localhost:5000${NC}${BLUE}              │${NC}"
echo -e "${BLUE}├─────────────────────────────────────────────────────┤${NC}"
echo -e "${BLUE}│${NC}  Logs: $LOGS_DIR${BLUE}                   │${NC}"
echo -e "${BLUE}│${NC}  Press ${YELLOW}CTRL+C${NC}${BLUE} to stop both servers               │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────┘${NC}"

# Wait for both processes
wait
