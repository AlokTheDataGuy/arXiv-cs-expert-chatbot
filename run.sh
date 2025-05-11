#!/bin/bash

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null
then
    echo "Starting Ollama..."
    ollama serve &
    sleep 5  # Give Ollama time to start
fi

# Start the backend server
echo "Starting backend server..."
cd backend
python run.py &
BACKEND_PID=$!

# Wait for the backend to start
sleep 5

# Start the frontend development server
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
    echo "Shutting down servers..."
    kill $FRONTEND_PID
    kill $BACKEND_PID
    exit 0
}

# Register the cleanup function for script termination
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "Servers are running. Press Ctrl+C to stop."
wait
