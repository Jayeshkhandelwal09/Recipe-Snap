from PIL import Image
import cv2
import numpy as np
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)

def validate_image(file: UploadFile) -> bool:
    """Validate uploaded image file"""
    try:
        # Check file extension
        if file.filename:
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in settings.allowed_extensions:
                logger.warning(f"Invalid file extension: {file_extension}")
                return False
        
        # Check file size
        if file.size and file.size > settings.max_file_size:
            logger.warning(f"File too large: {file.size} bytes")
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating image: {e}")
        return False

def process_image(image_path: str) -> str:
    """Process and optimize image for analysis"""
    try:
        # Load image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Resize if too large (for faster processing)
        max_size = 1024
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save processed image
        processed_path = image_path.replace(".", "_processed.")
        image.save(processed_path, "JPEG", quality=85)
        
        return processed_path
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return image_path  # Return original path if processing fails

def enhance_image_for_analysis(image_path: str) -> Optional[str]:
    """Enhance image quality for better ingredient detection"""
    try:
        # Read image with OpenCV
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Apply basic enhancements
        # 1. Increase contrast slightly
        alpha = 1.1  # Contrast control
        beta = 10    # Brightness control
        enhanced = cv2.convertScaleAbs(img_rgb, alpha=alpha, beta=beta)
        
        # 2. Apply slight sharpening
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        
        # Save enhanced image
        enhanced_path = image_path.replace(".", "_enhanced.")
        enhanced_pil = Image.fromarray(sharpened)
        enhanced_pil.save(enhanced_path, "JPEG", quality=90)
        
        return enhanced_path
    except Exception as e:
        logger.error(f"Error enhancing image: {e}")
        return None 