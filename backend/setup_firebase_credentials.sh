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

# Function to create a dummy service account file for development
create_dummy_credentials() {
    echo -e "${YELLOW}Creating dummy Firebase credentials for development mode...${NC}"
    
    # Create a dummy service account JSON
    cat > "healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json" << EOF
{
  "type": "service_account",
  "project_id": "healthcare-77135",
  "private_key_id": "dummy-key-for-development",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdummDq9gcHv9x\nyRvTDUJ+h3sJTmIZgHzQJ+fixcdQzVXxQdGeAXi5iZ7KBzfeCbrLAVvYGqH99EoW\nk3bBGrHQcAH5Xqrq3M3LnuiC25nRm3qQKe8weSz3K3QVSCMk+8XGMhCfmWor2ZPm\nLSFXyZiXJJs5VZ37FARYKsJxwfXhLunrYKxTCz4r5Zy7OqKjOgT+t9mAkDkK7i5z\n8fCjVxNlJKUqSn2VJNR8QDmY8HGOlMPeUhT3WIXd0ETtdKs3GEZLb7Fth3ALxCCH\nrxN+PECltEVbRvESvz6FYbgJTKRWGIVQfFTfN5OAGXpVYYnrIGdQVXA6lwXJpvsE\nK0ieDQYNAgMBAAECggEABiB5Wy5mQpqLFxhSEDWnIEtB8MJSFN9OyVrOa4ZmJCi4\nPROtZyHt2cAQ15GNfKYke5q6OA5aUbmxBEQxeYdUDbGBORBsxfCDrDLeCJJjnVe+\ntcN6OD4SY2Uf0DoqWjoqnHWZ7V/G9Bwe73wRH5bwXgRKSG4tBYFUZXb5ZnFnNNSh\n7sQhBSU3nuC2vj+mHZb75TpSsxQ3P5nPPU0c7lAFcFqvXb7HDNxPXhxTTfZXPrOu\nVWVH/nLfMTvz8N8sTa//nAA5IY5ZnxivUa2Qet2iW2T3QWFy9HeyA3RCxWJqQeT8\nQVUIwLEYCRLeXQCX37XwFQ6xvKEiUFm8U2Aw+TJYSQKBgQDNNpxnU2KPNdGvcupP\nmtS/5nLJGz3J42UxRU4XpWHwCVJbIFxvLpjjIlJ5fCn2wJF24Y9EB6CwXQTU+2J+\ncVg8WwKwg2MsYDNX3s7GhEg86y9N23MVbw1WnZwXGLPPdCKEHirFwHHl9Zi1ahBw\n9H7Y2bQB5LDLrxnWGwL3pQdyEwKBgQDF8f2Gy/adXJ9SjlAQbDr4Ve2nlKJJ3qSp\nNu3DjFcYuugFt2CffNhgCzqy5Q77C/JSOwvU9cL4c3Yp8vGl2SWBGz3RYMEZYih1\n1NCi19Q1Ziu7MPbZyr8/0KBWR7mGxIGQnrKsRH/GgfGAPTMRmPEVgXkIEGnRrNE9\n4DGTaHvpLwKBgBQJ5acfEzD5/EZ9eVPQs0W0NQMXTNHVQFwhBQQsXK1XcRsz3hZt\nVu3Q7KlZ95oQjOVZOpK0OlQAH4+KznbLV+Y3mtusxbvdJjsYyOdEfWUIbEj+UYVS\nN0tWKqUEcpOu0wktlQ6WInC3EDSgHyMJXD/NI0M4PfKSZJOOpfFnVQtLAoGAQ4dN\nL4VC3xOJszshdYlVMQnXc4WXFnRz3PCcbRmcNyJqrOOVdNKZKfUqzWLl5j9ENZWF\nfEXlA3F8g9CqDwyOVFJQbCp5s7NepicULQ+9sJcbSg9ASM5rDpmjrA2Rfh4QwAkA\nQk0zXjJPuRrYu5M+L8LW9TJSVzZlFfF+iBdkX+ECgYEAwIxl1XZ3iHLnXdGZKgLm\ns0OuXKvGYGJXkmLsb1yOWXLZ1X3+roQTVZNtGTMjsAo/lWG0A9m1UbPcKwvQslZq\nLOgXRKYmDIrXn6SNYpplYf8BFnXpKqBU5KbOzx2leO4wLlQJ8VyO8oqiV6aepW1a\nf5qcIUeyUZMeQxMHCQd8Jrg=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@healthcare-77135.iam.gserviceaccount.com",
  "client_id": "000000000000000000000",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40healthcare-77135.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
EOF

    echo -e "${GREEN}Created dummy credentials file:${NC} healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json"
    echo -e "${YELLOW}Note: This is for development only. Use real credentials in production.${NC}"
    
    # Set the path to the dummy credentials file
    cred_file="$(pwd)/healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json"
    
    # Create dev service account file too
    cp "healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json" "dev_service_account.json"
}

# Check if the user wants to use development mode
echo -e "${YELLOW}Do you want to use mock Firebase for development? (y/n)${NC}"
read -r use_mock

if [[ "$use_mock" == "y" || "$use_mock" == "Y" ]]; then
    create_dummy_credentials
    # Set environment variable to enable mock mode
    export FIREBASE_USE_MOCK=true
    echo "export FIREBASE_USE_MOCK=true" >> .env
    
    echo -e "\n${GREEN}Setup completed in development mode!${NC}"
    echo -e "The app will use mock Firebase implementations for testing."
    exit 0
fi

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
    echo -e "${YELLOW}Do you want to create dummy credentials for development? (y/n)${NC}"
    read -r create_dummy
    
    if [[ "$create_dummy" == "y" || "$create_dummy" == "Y" ]]; then
        create_dummy_credentials
        exit 0
    else
        exit 1
    fi
fi

# Create credential directory if it doesn't exist
cred_dir="$HOME/.config/firebase"
mkdir -p "$cred_dir"

# Copy the service account file
cred_file="$cred_dir/healthcare-service-account.json"
cp "$service_account_path" "$cred_file"
cp "$service_account_path" "healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json"
cp "$service_account_path" "dev_service_account.json"

# Update the environment variable
echo "export GOOGLE_APPLICATION_CREDENTIALS=\"$cred_file\"" >> "$HOME/.bashrc"
echo "export FIREBASE_USE_MOCK=false" >> .env

echo -e "\n${GREEN}Setup completed!${NC}"
echo -e "Service account credentials copied to: $cred_file"
echo -e "GOOGLE_APPLICATION_CREDENTIALS environment variable has been added to your .bashrc"
echo -e "${YELLOW}Important: Restart your terminal or run 'source ~/.bashrc' to apply the changes.${NC}\n"
echo -e "To test if everything is working, you can run the backend with:"
echo -e "  python main.py"
