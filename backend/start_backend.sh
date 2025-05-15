#!/bin/bash

# Install requirements
pip install -r requirements.txt --break-system-packages

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)
export ENVIRONMENT="development"

# Start the FastAPI server
python3 main.py
