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
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}Created .env file. Please edit it with your Firebase configuration.${NC}"
else
    echo -e "${YELLOW}.env file already exists. Skipping...${NC}"
fi

# Ask if user wants to set up Firebase credentials
echo -e "\n${YELLOW}Do you want to set up Firebase service account credentials? (y/n)${NC}"
read -r setup_firebase
if [[ "$setup_firebase" == "y" || "$setup_firebase" == "Y" ]]; then
    ./setup_firebase_credentials.sh
fi

echo -e "\n${GREEN}Initialization complete!${NC}"
echo -e "To start the backend server, run:"
echo -e "  source venv/bin/activate  # If not already activated"
echo -e "  python -m uvicorn main:app --reload"
echo -e "\nOnce running, you can access:"
echo -e "  API Documentation: http://localhost:8000/docs"
echo -e "  API Redoc: http://localhost:8000/redoc"
echo -e "  Health Check: http://localhost:8000/health"
