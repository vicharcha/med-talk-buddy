# Med Talk Buddy Backend

This is the backend server for Med Talk Buddy, a medical assistant application that uses AI/ML for various healthcare-related functionalities.

## Features

- FastAPI-based RESTful API
- Firebase Authentication
- ML/AI Integration with various models
- BMI Calculator
- Medical Chat Interface
- Vision Analysis for medical images
- Medical Records Management

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Firebase:
   - Place your Firebase service account key in the root directory
   - Name it as specified in the configuration or update the path in `core/config.py`

4. Set up environment variables:
   Create a `.env` file with the following:
   ```
   SECRET_KEY=your-secret-key
   FIREBASE_CREDENTIALS_PATH=path-to-firebase-credentials.json
   OPENAI_API_KEY=your-openai-api-key
   GOOGLE_API_KEY=your-google-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   DEEPSEEK_API_KEY=your-deepseek-api-key
   ```

5. Start the server:
   ```bash
   ./start_backend.sh
   ```

## API Documentation

Once the server is running, you can access:
- API documentation at: http://localhost:8000/docs
- Alternative documentation at: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── start_backend.sh          # Startup script
├── app/
│   ├── app.py               # FastAPI app instance
│   ├── api/                 # API routes
│   ├── core/                # Core configurations
│   ├── models/              # Data models
│   └── services/            # Business logic
└── models/                  # ML models
    ├── slm/                 # Language models
    └── vision/              # Vision models
```

## Testing

Run tests with:
```bash
pytest
```

## Development

For local development:
1. Set `ENVIRONMENT=development` in your environment
2. The system will use mock Firebase for authentication
3. Use the provided test data in `tests/data/`

## License

[MIT License](LICENSE)
