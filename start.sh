#!/bin/bash
# Start both backend and frontend servers for development.
# Usage: ./start.sh

set -e

echo "=== Starting Salary Management Tool ==="

# Backend
echo "Starting backend..."
cd backend
if [ ! -d "venv" ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

# Seed if DB is empty
if [ ! -f "salary_management.db" ]; then
  echo "Seeding database with 10,000 employees..."
  python seed.py
fi

uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Frontend
echo "Starting frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
  npm install
fi
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=== Servers running ==="
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
