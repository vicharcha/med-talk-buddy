#!/bin/bash

# Setup script for the MedTalkBuddy Backend
echo "Setting up MedTalkBuddy Backend..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Setup Firebase credentials
echo "Setting up Firebase credentials..."
bash setup_firebase_credentials.sh

# Run the server
echo "Starting the server..."
python main.py
