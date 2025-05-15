from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from typing import Dict, Any, Optional
from app.models.models import ChatRequest, ChatResponse
import datasets

class MedicalChatService:
    def __init__(self):
        # Initialize model and tokenizer
        self.model_name = "microsoft/phi-2"  # Using Phi-2 as it's currently available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                torch_dtype=torch.float16
            )
            self.chat = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto"
            )
            
            # Load medical context
            self._load_medical_context()
            
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            self.chat = None
    
    def _load_medical_context(self):
        """Load and prepare medical datasets for context"""
        from app.config.model_config import model_config
        
        self.medical_datasets = {}
        for dataset_name, dataset_path in model_config.DATASETS.items():
            try:
                # Split the dataset path into name and subset
                if "/" in dataset_path:
                    repo_name, *subset_parts = dataset_path.split("/")
                    if len(subset_parts) > 1:
                        dataset = datasets.load_dataset(
                            f"{repo_name}/{subset_parts[0]}", 
                            subset_parts[-1], 
                            split="train"
                        )
                    else:
                        dataset = datasets.load_dataset(repo_name, subset_parts[0], split="train")
                else:
                    dataset = datasets.load_dataset(dataset_path, split="train")
                    
                self.medical_datasets[dataset_name] = dataset
                print(f"Successfully loaded dataset: {dataset_name}")
            except Exception as e:
                print(f"Error loading dataset {dataset_name}: {str(e)}")
                continue
    
    def _create_prompt(self, user_input: str, context: str = "") -> str:
        """Create a prompt with medical context"""
        system_prompt = """You are MedTalkBuddy, an AI medical assistant with expertise in various medical fields including biology, clinical medicine, and healthcare. 
        Your knowledge comes from extensive medical datasets and training.
        
        Guidelines:
        1. Provide accurate, evidence-based medical information
        2. Always mention that you're an AI and encourage consulting healthcare professionals
        3. Be clear about limitations and uncertainties
        4. Focus on general medical knowledge and education
        5. Avoid making specific diagnoses
        
        Relevant Medical Context:
        {context}
        
        User Query: {query}
        
        Based on the medical context and my training, here is my response:
        """
        
        return system_prompt.format(
            query=user_input,
            context=context if context else "No specific medical context found for this query."
        )
    
    def _get_relevant_context(self, query: str) -> str:
        """Retrieve relevant medical context from loaded datasets"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        relevant_contexts = []
        
        # Process each dataset
        for dataset_name, dataset in self.medical_datasets.items():
            try:
                # Extract text from dataset (adjust based on actual dataset structure)
                if 'text' in dataset.features:
                    corpus = dataset['text']
                elif 'question' in dataset.features:
                    corpus = [f"{q} {a}" for q, a in zip(dataset['question'], dataset['answer'])]
                else:
                    continue
                
                # Create TF-IDF vectorizer
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(corpus)
                query_vec = vectorizer.transform([query])
                
                # Calculate similarity
                similarities = cosine_similarity(query_vec, tfidf_matrix)[0]
                
                # Get top 3 most relevant entries
                top_indices = np.argsort(similarities)[-3:][::-1]
                
                for idx in top_indices:
                    if similarities[idx] > 0.1:  # Similarity threshold
                        context = corpus[idx]
                        relevant_contexts.append(f"[{dataset_name}] {context}")
            
            except Exception as e:
                print(f"Error processing dataset {dataset_name}: {str(e)}")
                continue
        
        # Combine relevant contexts
        if relevant_contexts:
            return "\n".join(relevant_contexts[:5])  # Limit to top 5 most relevant contexts
        return ""
    
    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        """Generate a response to the user's medical query"""
        try:
            if not self.chat:
                raise Exception("Model not properly initialized")
            
            # Get relevant context from datasets
            context = self._get_relevant_context(request.message)
            
            # Create prompt with medical context
            prompt = self._create_prompt(request.message, context)
            
            # Generate response using model config settings
            from app.config.model_config import model_config
            response = self.chat(
                prompt,
                max_length=model_config.MAX_LENGTH,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )
            
            # Extract and clean response
            response_text = response[0]["generated_text"]
            response_text = response_text.split("Assistant:")[-1].strip()
            
            return ChatResponse(
                message=response_text,
                conversation_id=request.conversation_id or "new_session",
                additional_info={"model": self.model_name}
            )
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)
            return ChatResponse(
                message="I apologize, but I'm having trouble generating a response. Please try again.",
                conversation_id=request.conversation_id or "error_session",
                additional_info={"error": error_msg}
            )
