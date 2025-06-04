from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    app_name: str = "RecipeSnap API"
    debug: bool = True
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: set = {".jpg", ".jpeg", ".png", ".webp"}
    
    # Model configurations
    image_model_name: str = "nlpconnect/vit-gpt2-image-captioning"
    recipe_model_name: str = "microsoft/DialoGPT-medium"
    
    # Model settings
    use_gpu: bool = True  # Set to True if you have a GPU
    model_cache_dir: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True) 