#!/bin/bash

# Ralex V3 Launch Script
# Starts both the backend API and frontend web interface

echo "🚀 Starting Ralex V3 - AI Coding Assistant"
echo "=====================================\n"

# Check if required dependencies are available
echo "Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed"
    exit 1
fi

echo "✅ All dependencies found"

# Check if OPENROUTER_API_KEY is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  OPENROUTER_API_KEY environment variable not set"
    echo "   Please set it with: export OPENROUTER_API_KEY='your_key_here'"
    echo "   Continuing anyway for testing..."
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to cleanup on exit
cleanup() {
    echo "\n🛑 Shutting down Ralex V3..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✅ Cleanup complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the backend API server
echo "Starting Ralex V3 API server..."
cd /home/RPI3/ralex
python3 -m ralex_core.openai_api > logs/backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend API started (PID: $BACKEND_PID)"
    echo "   - API available at: http://localhost:8000"
    echo "   - Health check: http://localhost:8000/health"
    echo "   - WebSocket: ws://localhost:8000/ws/{session_id}"
else
    echo "❌ Failed to start backend API"
    echo "   Check logs/backend.log for details"
    exit 1
fi

# Start the frontend web interface
echo "Starting Ralex V3 web interface..."
cd /home/RPI3/ralex/ralex-frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

# Check if frontend started successfully
if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "✅ Frontend started (PID: $FRONTEND_PID)"
    echo "   - Web interface: http://localhost:3000"
else
    echo "❌ Failed to start frontend"
    echo "   Check logs/frontend.log for details"
    cleanup
    exit 1
fi

echo "\n🎉 Ralex V3 is now running!"
echo "=====================================\n"
echo "📱 Web Interface: http://localhost:3000"
echo "🔧 API Docs: http://localhost:8000/docs"
echo "💰 Budget tracking and voice input enabled"
echo "🧠 AgentOS integration active"
echo ""
echo "Features available:"
echo "  • 🎙️ Voice-to-text coding"
echo "  • 💰 Real-time budget tracking" 
echo "  • 🧠 Smart model selection"
echo "  • 📁 File context management"
echo "  • 🔄 WebSocket real-time updates"
echo ""
echo "Press Ctrl+C to stop all services"
echo "Logs: logs/backend.log, logs/frontend.log"
echo ""

# Wait for user interrupt
while true; do
    sleep 1
    
    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend process died unexpectedly"
        echo "   Check logs/backend.log for details"
        cleanup
        exit 1
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend process died unexpectedly"
        echo "   Check logs/frontend.log for details"
        cleanup
        exit 1
    fi
done