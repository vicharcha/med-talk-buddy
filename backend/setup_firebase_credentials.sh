#!/bin/bash

# This script helps in setting up Firebase service account credentials for backend authentication
# You need to have downloaded the service account JSON file from Firebase Console

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Firebase Service Account Setup${NC}"
echo -e "===============================\n"

# Check if GOOGLE_APPLICATION_CREDENTIALS env var is already set
if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo -e "${YELLOW}GOOGLE_APPLICATION_CREDENTIALS is already set to:${NC}"
    echo -e "$GOOGLE_APPLICATION_CREDENTIALS"
    echo -e "${YELLOW}Do you want to override it? (y/n)${NC}"
    read -r override
    if [[ "$override" != "y" && "$override" != "Y" ]]; then
        echo -e "${YELLOW}Keeping existing credentials. Setup aborted.${NC}"
        exit 0
    fi
fi

# Ask for the service account file path
echo -e "${YELLOW}Please enter the path to your Firebase service account JSON file:${NC}"
read -r service_account_path

# Validate the file exists
if [ ! -f "$service_account_path" ]; then
    echo -e "${RED}Error: File not found at $service_account_path${NC}"
    exit 1
fi

# Create credential directory if it doesn't exist
cred_dir="$HOME/.config/firebase"
mkdir -p "$cred_dir"

# Copy the service account file
cred_file="$cred_dir/healthcare-service-account.json"
cp "$service_account_path" "$cred_file"

# Update the environment variable
echo "export GOOGLE_APPLICATION_CREDENTIALS=\"$cred_file\"" >> "$HOME/.bashrc"

echo -e "\n${GREEN}Setup completed!${NC}"
echo -e "Service account credentials copied to: $cred_file"
echo -e "GOOGLE_APPLICATION_CREDENTIALS environment variable has been added to your .bashrc"
echo -e "${YELLOW}Important: Restart your terminal or run 'source ~/.bashrc' to apply the changes.${NC}\n"
echo -e "To test if everything is working, you can run the backend with:"
echo -e "  cd backend && python -m uvicorn main:app --reload"
