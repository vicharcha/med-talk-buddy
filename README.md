# MedTalkBuddy - Your Intelligent Healthcare Companion

MedTalkBuddy is a comprehensive AI-powered healthcare assistant that provides personalized health information, recommendations, and guidance. Combining a modern React frontend with a FastAPI backend and advanced ML-based responses, it offers an intuitive and informative healthcare chatbot experience.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)

## Table of Contents
- [Key Features](#key-features)
  - [Advanced BMI Calculator](#advanced-bmi-calculator)
  - [Interactive Healthcare Chat](#interactive-healthcare-chat)
  - [Smart Features](#smart-features)
  - [Security & Privacy](#security--privacy)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development](#development)
- [Technology Stack](#technology-stack)
- [Deployment](#deployment)
- [Demo & Documentation](#demo--documentation)
- [License & Credits](#license--credits)

## Key Features

### Advanced BMI Calculator
- Real-time unit conversion between metric (cm/kg) and imperial (ft-in/lbs)
- Detailed health risk assessment and recommendations
- Visual BMI scale with color-coded categories
- Personalized healthy weight range calculations
- Common measurement references for easy validation
- Comprehensive health context and limitations explanation

### Interactive Healthcare Chat
- AI-powered medical information and guidance
- Context-aware health recommendations
- Emergency alerts for critical symptoms
- Professional medical disclaimers
- Evidence-based medical information

### Smart Features
- **Intelligent Unit Conversion**: Seamless switching between metric and imperial units
- **Data Validation**: Extensive input validation with helpful error messages
- **Visual Feedback**: Color-coded health risk indicators
- **Personalized Analysis**: Individual BMI assessment and recommendations
- **Mobile-Friendly Design**: Responsive UI optimized for all devices

### Security & Privacy
- Secure user authentication via Firebase
- Data encryption and privacy protection
- HIPAA-compliant data handling
- Secure API endpoints

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
4. Start the backend server (FastAPI)
5. Start the frontend development server (Vite)

#### Environment Variables

Create a `.env` file in the root directory:

```env
# Frontend Environment Variables
VITE_API_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain
VITE_FIREBASE_PROJECT_ID=your_project_id

# Backend Environment Variables
GOOGLE_APPLICATION_CREDENTIALS=path/to/firebase-credentials.json
GOOGLE_API_KEY=your_google_api_key
PORT=8000
```

#### Health and BMI Guidelines

The BMI calculator follows WHO guidelines for adult BMI classifications:
- Severe Underweight: < 16.0
- Moderate Underweight: 16.0 - 16.9
- Mild Underweight: 17.0 - 18.4 
- Normal Weight: 18.5 - 24.9
- Overweight: 25.0 - 29.9
- Obesity Class I: 30.0 - 34.9
- Obesity Class II: 35.0 - 39.9
- Obesity Class III: ≥ 40.0

Note: BMI calculations are intended for adults 20 years and older. Different criteria apply for children and teens.

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

### Frontend Architecture
- **Core Technologies**:
  - React 18.3
  - TypeScript 5.5
  - Vite 5.4 for blazing-fast development
  - Tailwind CSS for responsive styling
  
- **UI Components**:
  - shadcn-ui for consistent design
  - Radix UI primitives for accessibility
  - Custom BMI visualization components
  - Responsive layout system

- **State Management & Data Flow**:
  - React Query for API data management
  - Context API for global state
  - Custom hooks for business logic
  - Firebase Auth for user management

### Backend Architecture
- **Core Technologies**:
  - Python 3.12+
  - FastAPI for high-performance API
  - Pydantic for data validation
  - Firebase Admin SDK for auth

- **AI & ML Components**:
  - TensorFlow/scikit-learn for model training
  - NLTK for natural language processing
  - Custom medical response generation
  - Health risk assessment algorithms

- **Data Processing**:
  - NumPy for numerical computations
  - Pandas for data manipulation
  - Custom health metrics calculation
  - Secure data validation pipeline

## Deployment

### Deployment Options

1. **Traditional Deployment**:
   - Frontend: Vercel, Netlify, or any Node.js hosting
   - Backend: Cloud Run, Heroku, or any Python hosting
   - Database: Firebase Realtime Database

2. **Containerized Deployment**:
   ```bash
   # Build Docker images
   docker-compose build

   # Run the application
   docker-compose up
   ```

3. **Serverless Deployment**:
   - Frontend: Static hosting (Vercel/Netlify)
   - Backend: Cloud Functions
   - Auth: Firebase Authentication

### System Requirements
- Node.js 16+ for frontend
- Python 3.12+ for backend
- 2GB RAM minimum
- 1GB storage space

## Demo & Documentation

### Live Demo
Check out our live demo screencast to see MedTalkBuddy in action: [Watch Demo](Screencast%20from%202025-05-17%2000-02-57.webm)

### API Documentation
Access our API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development Guide

### Code Style & Standards
- Follow [ESLint](https://eslint.org/) configuration for TypeScript/React
- Use [Black](https://black.readthedocs.io/) for Python code formatting
- Commit messages should follow [Conventional Commits](https://www.conventionalcommits.org/)

### Running Tests
```bash
# Frontend tests
npm test
npm run test:coverage

# Backend tests
cd backend
pytest
pytest --cov=app tests/
```

### Contributing Guidelines
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Submit a pull request

## Support & Community

### Get Help
- Create an issue on GitHub
- Join our [Discord community](https://discord.gg/medtalkbuddy)
- Email: support@medtalkbuddy.com

### Stay Updated
- Follow us on [Twitter](https://twitter.com/medtalkbuddy)
- Subscribe to our newsletter

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with assistance from GitHub Copilot
- Medical information validated by healthcare professionals
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- BMI calculations based on WHO guidelines
