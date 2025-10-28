"""
Image processing and handling for the Jild AI application.
"""

import base64
import io
from typing import Tuple, Optional
from PIL import Image
import streamlit as st
from src.config import config
from src.utils import display_error


class ImageHandler:
    """Handle image processing, validation, and encoding."""
    
    @staticmethod
    def validate_image(image_file) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded image file.
        
        Args:
            image_file: Uploaded file object from Streamlit
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if image_file is None:
            return False, "No image file provided"
        
        # Check file size
        file_size_mb = image_file.size / (1024 * 1024)
        if file_size_mb > config.max_file_size_mb:
            return False, f"File size ({file_size_mb:.1f}MB) exceeds maximum allowed size ({config.max_file_size_mb}MB)"
        
        # Check file format
        file_extension = image_file.name.split('.')[-1].lower()
        if file_extension not in config.supported_formats:
            return False, f"File format '.{file_extension}' not supported. Supported formats: {', '.join(config.supported_formats)}"
        
        return True, None
    
    @staticmethod
    def load_image(image_file) -> Optional[Image.Image]:
        """
        Load image from uploaded file.
        
        Args:
            image_file: Uploaded file object
            
        Returns:
            PIL Image object or None if loading fails
        """
        try:
            image = Image.open(image_file)
            # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            display_error("Failed to load image", e)
            return None
    
    @staticmethod
    def resize_image(image: Image.Image, max_size: Tuple[int, int] = None) -> Image.Image:
        """
        Resize image if it exceeds maximum dimensions while maintaining aspect ratio.
        
        Args:
            image: PIL Image object
            max_size: Maximum dimensions (width, height)
            
        Returns:
            Resized PIL Image object
        """
        if max_size is None:
            max_size = config.max_image_size
        
        # Check if resizing is needed
        if image.width <= max_size[0] and image.height <= max_size[1]:
            return image
        
        # Calculate new dimensions maintaining aspect ratio
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    @staticmethod
    def image_to_base64(image: Image.Image, format: str = 'JPEG') -> str:
        """
        Convert PIL Image to base64 encoded string.
        
        Args:
            image: PIL Image object
            format: Image format for encoding
            
        Returns:
            Base64 encoded string
        """
        buffered = io.BytesIO()
        image.save(buffered, format=format, quality=95)
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return img_base64
    
    @staticmethod
    def prepare_image_for_api(image_file) -> Optional[Tuple[Image.Image, str]]:
        """
        Complete image processing pipeline for API submission.
        
        Args:
            image_file: Uploaded file object
            
        Returns:
            Tuple of (PIL Image, base64 string) or None if processing fails
        """
        # Validate image
        is_valid, error_msg = ImageHandler.validate_image(image_file)
        if not is_valid:
            display_error(error_msg)
            return None
        
        # Load image
        image = ImageHandler.load_image(image_file)
        if image is None:
            return None
        
        # Resize if needed
        image = ImageHandler.resize_image(image)
        
        # Convert to base64
        try:
            base64_image = ImageHandler.image_to_base64(image)
            return image, base64_image
        except Exception as e:
            display_error("Failed to process image", e)
            return None
    
    @staticmethod
    def get_image_info(image: Image.Image) -> dict:
        """
        Get information about the image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with image information
        """
        return {
            'width': image.width,
            'height': image.height,
            'format': image.format,
            'mode': image.mode,
        }

