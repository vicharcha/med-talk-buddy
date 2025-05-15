from pydantic_settings import BaseSettings
import torch
class ModelConfig(BaseSettings):
    MODEL_ID: str = "microsoft/phi-2"  # Using Phi-2 as it's currently available
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    MAX_LENGTH: int = 2048
    
    # Dataset configurations
    DATASETS = {
        "biology": "MMMU/MMMU/Biology",
        "basic_medical": "MMMU/MMMU/Basic_Medical_Science",
        "chemistry": "MMMU/MMMU/Chemistry",
        "clinical_medicine": "MMMU/MMMU/Clinical_Medicine",
        "college_medicine": "cais/mmlu/college_medicine",
        "clinical_knowledge": "cais/mmlu/clinical_knowledge",
        "nutrition": "cais/mmlu/nutrition",
        "philosophy": "cais/mmlu/philosophy",
        "human_aging": "cais/mmlu/human_aging",
        "human_sexuality": "cais/mmlu/human_sexuality",
        "medical_genetics": "cais/mmlu/medical_genetics"
    }

model_config = ModelConfig()
