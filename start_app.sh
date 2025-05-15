#!/bin/bash

# Start MedTalkBuddy Application (both frontend and backend)
echo "Starting MedTalkBuddy Application..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v npm &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js and try again."
    exit 1
fi

# Start the backend server in the background
echo "Starting backend server..."
cd backend
# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
# Install dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Check if the ML model exists, if not train it
if [ ! -f "models/medical_model.h5" ]; then
    echo "Training ML model..."
    python train_model.py
fi

# Start the backend server
echo "Starting FastAPI server..."
python main.py &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Change back to the root directory
cd ..

# Start the frontend in the foreground
echo "Starting frontend..."
npm run dev

# When the frontend is stopped, also stop the backend
echo "Stopping backend server..."
kill $BACKEND_PID
