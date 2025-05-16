
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

# Create the model directory if it doesn't exist
mkdir -p backend/model

# Set up backend
cd backend
echo "Setting up virtual environment..."
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

# Check if we need to train the model
if [ "$1" == "--train-model" ]; then
    echo "Starting model training... This may take a long time depending on your hardware."
    python train_model.py
    echo "Model training completed."
    exit 0
fi

# Start the backend server
echo "Starting FastAPI server..."
PYTHONPATH=$(pwd) python main.py &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Change back to the root directory
cd ..

# Start the frontend in the foreground
echo "Starting frontend..."
npm install  # Install frontend dependencies
npm run dev

# When the frontend is stopped, also stop the backend
echo "Stopping backend server..."
kill $BACKEND_PID

echo ""
echo "==================================================================="
echo "NOTE: To train the medical model, run: ./start_app.sh --train-model"
echo "==================================================================="
