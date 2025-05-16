# MedTalkBuddy - Your Healthcare Companion

MedTalkBuddy is an AI-powered healthcare assistant that provides personalized health information, recommendations, and guidance. It combines a React frontend with a FastAPI backend and ML-based responses to create a comprehensive healthcare chatbot experience.

## Features

- **Interactive Chat Interface**: Talk to the AI assistant about your health concerns
- **Personalized Health Recommendations**: Get recommendations based on your health data
- **BMI Calculator**: Calculate and track your BMI
- **User Authentication**: Secure user accounts with Firebase
- **Mobile-Friendly Design**: Responsive UI that works on all devices

## Project Structure

The project consists of two main parts:

1. **Frontend** (React, TypeScript, Tailwind CSS)
   - Modern UI components using shadcn-ui
   - Firebase authentication integration
   - Responsive design for all devices

2. **Backend** (Python, FastAPI)
   - RESTful API endpoints for chat and health data
   - ML-based response generation
   - Firebase integration for data storage and auth
   - Health recommendation engine

## Getting Started

### Prerequisites

- Node.js 16+ and npm/yarn/bun
- Python 3.8+
- Firebase account (optional for development)

### Quick Start

The easiest way to start the application is using the provided script:

```bash
# Make the script executable if needed
chmod +x start_app.sh

# Run the application
./start_app.sh
```

This will:
1. Set up the Python environment for the backend
2. Install all dependencies
3. Train the ML model if needed
4. Start the backend server
5. Start the frontend development server

### Manual Setup

#### Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Firebase credentials (you can choose development mode)
./setup_firebase_credentials.sh

# Train the ML model
python train_model.py

# Start the backend server
python main.py
```

#### Frontend Setup

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```

## Development

### Backend API

The backend provides the following API endpoints:

- `/api/v1/chat/messages` - Send and receive chat messages
- `/api/v1/chat/recommendations` - Get personalized health recommendations
- `/api/v1/bmi` - Calculate and store BMI data
- `/api/v1/users` - User management

### Frontend Routes

- `/` - Home page
- `/chat` - Chat with MedTalkBuddy
- `/bmi` - BMI Calculator
- `/login` - User login
- `/register` - User registration
- `/profile` - User profile

## Technology Stack

- **Frontend**:
  - React
  - TypeScript
  - Tailwind CSS
  - shadcn-ui components
  - Firebase Auth
  - Vite

- **Backend**:
  - Python
  - FastAPI
  - Firebase Admin SDK
  - TensorFlow/scikit-learn
  - NLTK

## Deployment

You can deploy the application to any platform that supports:
- Node.js for the frontend
- Python for the backend
- Or use Docker for containerized deployment


# Demo

Check out the live demo at [MedTalkBuddy Demo](/home/kasinadhsarma/med-talk-buddy/Screencast%20from%202025-05-17%2000-02-57.webm).

## License

This project was created using Lovable's tools and services.

## Acknowledgments

Built with the help of Lovable and GitHub Copilot.
