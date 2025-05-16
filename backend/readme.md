
# MedTalkBuddy Backend

This is the backend for the MedTalkBuddy application, a healthcare AI assistant that provides medical information and advice.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python main.py
   ```
   Or use the start script:
   ```
   ./start_app.sh
   ```

## Training the Model

To train the medical model using the specified datasets:

```
./start_app.sh --train-model
```

This will:
1. Download the specified datasets from Hugging Face
2. Preprocess the data
3. Train a custom medical model
4. Save the model in H5 format

Datasets used for training:
- MMMU/Biology
- MMMU/Basic_Medical_Science
- MMMU/Chemistry
- MMMU/Clinical_Medicine
- MMLU/college_medicine
- MMLU/clinical_knowledge
- MMLU/nutrition
- MMLU/philosophy
- MMLU/human_aging
- MMLU/human_sexuality
- MMLU/medical_genetics

## API Endpoints

- `GET /api/v1/health` - Check if the backend is running and if the model is loaded
- `POST /api/v1/chat/send` - Send a message to the AI assistant
- `GET /api/v1/chat/history/{conversation_id}` - Get conversation history

## Architecture

The backend uses:
- FastAPI for the API server
- Google's Gemini API for the current LLM integration
- Custom trained model (coming soon)
- Firebase for authentication

## Notes

- The system currently uses Google's Gemini API but will be updated to use the custom trained model once it's ready.
- All conversation history is stored temporarily and not persisted across server restarts.
