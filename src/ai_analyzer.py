"""
AI model integration for skin analysis.
Supports OpenRouter API (for GPT-4V, Claude, Gemini) and Hugging Face Inference API.
"""

import json
import logging
from typing import Optional, Dict
import requests
from openai import OpenAI
from src.config import config
from src.utils import get_skin_analysis_prompt


class AIAnalyzer:
    """AI-powered skin analysis using multimodal language models."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_with_openrouter(self, base64_image: str, model_id: str) -> Dict:
        """
        Analyze skin image using OpenRouter API.

        Args:
            base64_image: Base64 encoded image string
            model_id: Model identifier (e.g., 'openai/gpt-4o')

        Returns:
            Dictionary with analysis results
        """
        try:
            # Initialize OpenAI client with OpenRouter
            # Explicitly set only the required parameters to avoid conflicts
            client = OpenAI(
                base_url=config.openrouter_base_url,
                api_key=config.openrouter_api_key,
                default_headers={
                    "HTTP-Referer": "https://jildai.app",
                    "X-Title": "Jild AI"
                }
            )
            
            # Prepare the message with image
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": get_skin_analysis_prompt()
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            # Make API call
            self.logger.info(f"Calling OpenRouter API with model: {model_id}")
            response = client.chat.completions.create(
                model=model_id,
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
            )
            
            # Extract analysis from response
            analysis = response.choices[0].message.content
            
            return {
                'success': True,
                'analysis': analysis,
                'model': model_id,
                'provider': 'OpenRouter'
            }
            
        except Exception as e:
            self.logger.error(f"OpenRouter API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': model_id,
                'provider': 'OpenRouter'
            }
    
    def analyze_with_huggingface(self, base64_image: str, model_id: str) -> Dict:
        """
        Analyze skin image using Hugging Face Inference API.
        
        Args:
            base64_image: Base64 encoded image string
            model_id: Model identifier (e.g., 'llava-hf/llava-v1.6-34b-hf')
            
        Returns:
            Dictionary with analysis results
        """
        try:
            import base64
            
            # Prepare API endpoint
            api_url = f"{config.huggingface_api_url}/{model_id}"
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {config.huggingface_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare payload
            # For vision-language models, we need to send both image and text
            payload = {
                "inputs": {
                    "image": base64_image,
                    "text": get_skin_analysis_prompt()
                },
                "parameters": {
                    "max_new_tokens": 2000,
                    "temperature": 0.7,
                }
            }
            
            self.logger.info(f"Calling Hugging Face API with model: {model_id}")
            
            # Make API call
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            # Extract text from response (format varies by model)
            if isinstance(result, list) and len(result) > 0:
                analysis = result[0].get('generated_text', str(result))
            elif isinstance(result, dict):
                analysis = result.get('generated_text', result.get('text', str(result)))
            else:
                analysis = str(result)
            
            return {
                'success': True,
                'analysis': analysis,
                'model': model_id,
                'provider': 'Hugging Face'
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Hugging Face API request error: {str(e)}")
            error_msg = str(e)
            
            # Try to extract more detailed error from response
            try:
                if hasattr(e, 'response') and e.response is not None:
                    error_detail = e.response.json()
                    if 'error' in error_detail:
                        error_msg = error_detail['error']
            except:
                pass
            
            return {
                'success': False,
                'error': error_msg,
                'model': model_id,
                'provider': 'Hugging Face'
            }
        except Exception as e:
            self.logger.error(f"Hugging Face API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': model_id,
                'provider': 'Hugging Face'
            }
    
    def analyze_skin(self, base64_image: str, model_name: str, model_id: str) -> Dict:
        """
        Analyze skin image using the specified model.
        
        Args:
            base64_image: Base64 encoded image string
            model_name: Display name of the model
            model_id: Model identifier for API
            
        Returns:
            Dictionary with analysis results
        """
        # Determine which API to use based on model name prefix
        if model_name.startswith("🔒"):
            # OpenRouter model
            return self.analyze_with_openrouter(base64_image, model_id)
        elif model_name.startswith("🤗"):
            # Hugging Face model
            return self.analyze_with_huggingface(base64_image, model_id)
        else:
            return {
                'success': False,
                'error': 'Unknown model provider',
                'model': model_id,
                'provider': 'Unknown'
            }


# Global analyzer instance
analyzer = AIAnalyzer()

