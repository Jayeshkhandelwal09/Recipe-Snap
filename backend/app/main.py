from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from .api.routes import router
from .core.config import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered cooking assistant that analyzes fridge contents and suggests recipes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
os.makedirs(settings.upload_dir, exist_ok=True)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to RecipeSnap API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("🍳 RecipeSnap API is starting up...")
    logger.info(f"Upload directory: {settings.upload_dir}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Image model: {settings.image_model_name}")
    logger.info(f"Recipe model: {settings.recipe_model_name}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("RecipeSnap API is shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 