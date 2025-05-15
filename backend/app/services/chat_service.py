from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from app.models.models import ChatRequest, ChatResponse
import datasets

class ChatService:
    def __init__(self):
        """Initialize the chat service with medical AI models"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "microsoft/phi-4"  # Using Phi-2 as base model
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.datasets = {}
        self.initialize_service()
    
    def initialize_service(self):
        """Initialize models and datasets"""
        try:
            print(f"Initializing chat service using device: {self.device}")
            
            # Initialize tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                torch_dtype=torch.float16
            )
            
            # Setup generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto"
            )
            
            # Load medical datasets
            self._load_datasets()
            
            print("Chat service initialized successfully")
            
        except Exception as e:
            print(f"Error initializing chat service: {str(e)}")
            self.pipeline = None
    
    def _load_datasets(self):
        """Load medical datasets for context"""
        try:
            datasets_to_load = [
                ("MMMU/MMMU", "Biology"),
                ("MMMU/MMMU", "Basic_Medical_Science"),
                ("MMMU/MMMU", "Clinical_Medicine"),
                ("cais/mmlu", "college_medicine"),
                ("cais/mmlu", "clinical_knowledge")
            ]
            
            for dataset_name, subset in datasets_to_load:
                try:
                    self.datasets[subset] = datasets.load_dataset(
                        dataset_name,
                        subset,
                        split="train"
                    )
                except Exception as e:
                    print(f"Error loading dataset {dataset_name}/{subset}: {str(e)}")
        
        except Exception as e:
            print(f"Error in dataset loading: {str(e)}")
    
    def _create_prompt(self, message: str) -> str:
        """Create a medical context-aware prompt"""
        return f"""You are MedTalkBuddy, an AI medical assistant with expertise in various medical fields.
        You have been trained on extensive medical datasets and provide accurate, evidence-based information.
        
        Important guidelines:
        1. Always be clear that you're an AI assistant
        2. Encourage consulting healthcare professionals for specific medical advice
        3. Base responses on scientific evidence
        4. Focus on general medical knowledge and education
        5. Be clear about limitations and uncertainties
        
        User Question: {message}
        
        Medical Assistant Response:"""

    async def get_response(self, request: ChatRequest) -> ChatResponse:
        """Generate a response to the user's medical query"""
        try:
            if not self.pipeline:
                raise Exception("Chat service not properly initialized")
            
            # Create context-aware prompt
            prompt = self._create_prompt(request.message)
            
            # Generate response
            response = self.pipeline(
                prompt,
                max_length=1000,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )
            
            # Extract and clean response
            generated_text = response[0]["generated_text"]
            assistant_response = generated_text.split("Medical Assistant Response:")[-1].strip()
            
            return ChatResponse(
                message=assistant_response,
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                additional_info={
                    "model": self.model_name,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health status of the chat service"""
        return {
            "status": "healthy" if self.pipeline is not None else "unavailable",
            "model": self.model_name,
            "device": self.device,
            "timestamp": datetime.utcnow().isoformat(),
            "datasets_loaded": list(self.datasets.keys())
        }
