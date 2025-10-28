"""
Utility functions for the Jild AI application.
"""

import logging
from typing import Optional
import streamlit as st


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def display_error(message: str, exception: Optional[Exception] = None):
    """
    Display error message to user and log it.
    
    Args:
        message: Error message to display
        exception: Optional exception object for logging
    """
    st.error(f"❌ {message}")
    if exception:
        logging.error(f"{message}: {str(exception)}")
        # Show detailed error in expander for debugging
        with st.expander("🔍 Error Details"):
            st.code(str(exception))
    else:
        logging.error(message)


def display_success(message: str):
    """
    Display success message to user.
    
    Args:
        message: Success message to display
    """
    st.success(f"✅ {message}")


def display_info(message: str):
    """
    Display info message to user.
    
    Args:
        message: Info message to display
    """
    st.info(f"ℹ️ {message}")


def display_warning(message: str):
    """
    Display warning message to user.
    
    Args:
        message: Warning message to display
    """
    st.warning(f"⚠️ {message}")


def format_analysis_result(result: dict) -> str:
    """
    Format the analysis result for display.
    
    Args:
        result: Analysis result dictionary
        
    Returns:
        Formatted markdown string
    """
    return result.get('analysis', 'No analysis available')


def get_skin_analysis_prompt() -> str:
    """
    Get the specialized prompt for skin analysis.
    
    Returns:
        Prompt string for the AI model
    """
    return """You are an expert dermatologist and skincare specialist. Analyze the provided skin image carefully and provide a comprehensive assessment.

            Please provide your analysis in the following structured format:

            ## 🔍 Skin Analysis

            ### Detected Conditions
            List any visible skin conditions, concerns, or issues you observe (e.g., acne, dryness, oiliness, redness, dark spots, fine lines, uneven texture, etc.)

            ### Skin Type Assessment
            Identify the apparent skin type (e.g., oily, dry, combination, normal, sensitive)

            ### Severity Assessment
            For each detected condition, rate the severity as: Mild, Moderate, or Severe

            ## 💡 Recommendations

            ### Recommended Skincare Routine
            Provide a step-by-step daily skincare routine:
            1. **Morning Routine**
            2. **Evening Routine**

            ### Product Recommendations
            Suggest specific types of products that would be beneficial:
            - Cleanser type
            - Moisturizer type
            - Treatment products (serums, spot treatments, etc.)
            - Sun protection
            - Any additional products

            ### Lifestyle & Prevention Tips
            Provide 3-5 actionable tips for maintaining healthy skin

            ## ⚠️ Important Notes
            - Mention any concerns that might require professional medical attention
            - Add any precautions or warnings

            Be specific, helpful, and professional. If the image quality is not sufficient for a proper analysis, mention that. Always recommend consulting with a dermatologist for serious concerns."""

