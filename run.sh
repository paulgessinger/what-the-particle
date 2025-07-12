#!/bin/bash

# Particle Explorer - Startup Script
echo "🚀 Starting Particle Explorer..."

# Check if Python and Node are available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed."
    exit 1
fi

# Function to kill background processes on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup SIGINT SIGTERM

# Check and install backend dependencies
echo "📦 Checking backend dependencies..."
cd ..
if ! command -v uv &> /dev/null; then
    echo "🔧 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "🔧 Installing Python dependencies with uv..."
uv sync > /dev/null 2>&1

# Start backend server
echo "🐍 Starting FastAPI backend on http://localhost:8000..."
uv run python -m backend.main &
BACKEND_PID=$!

# Give backend time to start
sleep 2

# Check and install frontend dependencies
echo "📦 Checking frontend dependencies..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "🔧 Installing npm dependencies..."
    npm install
fi

# Start frontend server
echo "⚡ Starting SvelteKit frontend on http://localhost:5173..."
npm run dev &
FRONTEND_PID=$!

# Give frontend time to start
sleep 3

echo ""
echo "✅ Particle Explorer is running!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID