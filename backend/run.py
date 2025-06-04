#!/usr/bin/env python3
"""
RecipeSnap Backend Server
Run this script to start the FastAPI server
"""

import uvicorn

if __name__ == "__main__":
    print("🍳 Starting RecipeSnap API Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/api/v1/health")
    print("⚡ Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 