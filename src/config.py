"""
Configuration management for Jild AI application.
Handles API keys and model settings from environment variables or Streamlit secrets.
"""

import os
from typing import Optional
import streamlit as st


class Config:
    """Configuration manager for API keys and application settings."""
    
    def __init__(self):
        self.openrouter_api_key = self._get_secret("OPENROUTER_API_KEY")
        self.huggingface_api_key = self._get_secret("HUGGINGFACE_API_KEY")
        
        # Model configurations
        # Currently using Qwen as a wrapper to demonstrate core functionality
        # TODO: Replace with custom Jild AI model
        self.openrouter_models = {
            "Qwen2.5": "qwen/qwen2.5-vl-32b-instruct:free",
            # "GPT-4o": "openai/gpt-4o",
            # "GPT-4 Vision": "openai/gpt-4-vision-preview",
            # "Claude 3 Sonnet": "anthropic/claude-3-sonnet",
            # "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
            # "Google Gemini Pro Vision": "google/gemini-pro-vision",
        }

        # Hugging Face models (commented out for now)
        # self.huggingface_models = {
        #     "Llava v1.6 (34B)": "llava-hf/llava-v1.6-34b-hf",
        #     "Llava v1.6 (Mistral 7B)": "llava-hf/llava-v1.6-mistral-7b-hf",
        # }
        self.huggingface_models = {}
        
        # API endpoints
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self.huggingface_api_url = "https://api-inference.huggingface.co/models"
        
        # Image settings
        self.max_image_size = (1024, 1024)  # Max dimensions
        self.max_file_size_mb = 10  # Max file size in MB
        self.supported_formats = ['jpg', 'jpeg', 'png', 'webp']
    
    def _get_secret(self, key: str) -> Optional[str]:
        """
        Get secret from Streamlit secrets or environment variables.
        
        Args:
            key: The secret key to retrieve
            
        Returns:
            The secret value or None if not found
        """
        # Try Streamlit secrets first (for cloud deployment)
        try:
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass
        
        # Fall back to environment variables (for local development)
        return os.getenv(key)
    
    def is_openrouter_configured(self) -> bool:
        """Check if OpenRouter API key is configured."""
        return self.openrouter_api_key is not None and len(self.openrouter_api_key) > 0
    
    def is_huggingface_configured(self) -> bool:
        """Check if Hugging Face API key is configured."""
        return self.huggingface_api_key is not None and len(self.huggingface_api_key) > 0
    
    def get_available_models(self) -> dict:
        """
        Get available models based on configured API keys.
        
        Returns:
            Dictionary of available models
        """
        available = {}
        
        if self.is_openrouter_configured():
            available.update({f"🔒 {k}": v for k, v in self.openrouter_models.items()})
        
        if self.is_huggingface_configured():
            available.update({f"🤗 {k}": v for k, v in self.huggingface_models.items()})
        
        return available


# Global config instance
config = Config()

