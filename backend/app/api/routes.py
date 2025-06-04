from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
from typing import List
import shutil
import logging

from ..models.image_analyzer import ImageAnalyzer
from ..models.recipe_generator import RecipeGenerator
from ..core.config import settings
from ..utils.image_processing import validate_image, process_image

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize models (lazy loading)
image_analyzer = None
recipe_generator = None

def get_image_analyzer():
    """Get or initialize image analyzer"""
    global image_analyzer
    if image_analyzer is None:
        logger.info("Initializing image analyzer...")
        image_analyzer = ImageAnalyzer()
    return image_analyzer

def get_recipe_generator():
    """Get or initialize recipe generator"""
    global recipe_generator
    if recipe_generator is None:
        logger.info("Initializing recipe generator...")
        recipe_generator = RecipeGenerator()
    return recipe_generator

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded image and extract ingredients"""
    try:
        logger.info(f"Received image upload: {file.filename}")
        
        # Validate file
        if not validate_image(file):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Create upload directory if it doesn't exist
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(exist_ok=True)
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix.lower() if file.filename else ".jpg"
        file_path = upload_dir / f"{file_id}{file_extension}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Saved file to: {file_path}")
        
        # Process image
        processed_path = process_image(str(file_path))
        
        # Analyze image
        analyzer = get_image_analyzer()
        analysis_result = analyzer.analyze_image(processed_path)
        
        # Clean up files
        try:
            os.remove(file_path)
            if processed_path != str(file_path):
                os.remove(processed_path)
        except Exception as e:
            logger.warning(f"Error cleaning up files: {e}")
        
        logger.info(f"Analysis result: {analysis_result}")
        return JSONResponse(content=analysis_result)
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.post("/generate-recipes")
async def generate_recipes(request: dict):
    """Generate recipes based on ingredients"""
    try:
        ingredients = request.get("ingredients", [])
        logger.info(f"Generating recipes for ingredients: {ingredients}")
        
        if not ingredients:
            raise HTTPException(status_code=400, detail="No ingredients provided")
        
        # Generate recipes
        generator = get_recipe_generator()
        recipes = generator.generate_recipes(ingredients)
        
        result = {
            "success": True,
            "recipes": recipes,
            "total": len(recipes)
        }
        
        logger.info(f"Generated {len(recipes)} recipes")
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error generating recipes: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recipes: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "message": "RecipeSnap API is running",
        "version": "1.0.0"
    }

@router.get("/models/status")
async def models_status():
    """Check the status of AI models"""
    try:
        # Check if models are initialized
        image_status = "loaded" if image_analyzer is not None else "not loaded"
        recipe_status = "loaded" if recipe_generator is not None else "not loaded"
        
        return {
            "image_analyzer": image_status,
            "recipe_generator": recipe_status,
            "status": "ready"
        }
    except Exception as e:
        logger.error(f"Error checking model status: {e}")
        return {
            "image_analyzer": "error",
            "recipe_generator": "error",
            "status": "error",
            "error": str(e)
        }

@router.post("/models/load")
async def load_models():
    """Preload all models"""
    try:
        logger.info("Loading all models...")
        
        # Load image analyzer
        analyzer = get_image_analyzer()
        
        # Load recipe generator
        generator = get_recipe_generator()
        
        return {
            "status": "success",
            "message": "All models loaded successfully",
            "models": {
                "image_analyzer": "loaded",
                "recipe_generator": "loaded"
            }
        }
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading models: {str(e)}")

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to RecipeSnap API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze_image": "/api/v1/analyze-image",
            "generate_recipes": "/api/v1/generate-recipes",
            "health": "/api/v1/health",
            "models_status": "/api/v1/models/status"
        }
    } 