#!/bin/bash

# This script initializes the backend environment and helps with Firebase setup

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Healthcare API Backend Initialization${NC}"
echo -e "===================================\n"

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo -e "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo -e "${RED}Error: pip is not installed.${NC}"
    echo -e "Please install pip and try again."
    exit 1
fi

# Create a virtual environment
echo -e "${YELLOW}Creating a virtual environment...${NC}"
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to create virtual environment.${NC}"
    exit 1
fi

# Activate the virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to activate virtual environment.${NC}"
    exit 1
fi

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install requirements.${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << EOF
# Firebase configuration
FIREBASE_PROJECT_ID=healthcare-77135
FIREBASE_STORAGE_BUCKET=healthcare-77135.appspot.com
FIREBASE_API_KEY=AIzaSyDH687LJ8huxt_zpE4TYWqB9OsCLTH4HDw
FIREBASE_AUTH_DOMAIN=healthcare-77135.firebaseapp.com
FIREBASE_MESSAGING_SENDER_ID=867221601164
FIREBASE_APP_ID=1:867221601164:web:e094a34d9f052d58d2f41c

# Backend configuration
API_PREFIX=/api/v1
DEBUG=False
SECRET_KEY=your-super-secret-key-for-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Cloud credentials path
GOOGLE_APPLICATION_CREDENTIALS=healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json
EOF
    echo -e "${GREEN}Created .env file with Firebase configuration.${NC}"
else
    echo -e "${YELLOW}.env file already exists. Skipping...${NC}"
fi

# Set up Firebase credentials
echo -e "\n${YELLOW}Setting up Firebase credentials...${NC}"
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json
echo -e "${GREEN}Firebase credentials set to: $GOOGLE_APPLICATION_CREDENTIALS${NC}"

echo -e "\n${GREEN}Initialization complete!${NC}"
echo -e "To start the backend server, run:"
echo -e "  source venv/bin/activate  # If not already activated"
echo -e "  python -m uvicorn main:app --reload"
echo -e "\nOnce running, you can access:"
echo -e "  API Documentation: http://localhost:8000/docs"
echo -e "  API Redoc: http://localhost:8000/redoc"
echo -e "  Health Check: http://localhost:8000/health"
