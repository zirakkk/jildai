"""
Jild AI - Skin Health Detection and Skincare Recommendation App
Main Streamlit application file
"""

import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Jild AI - Skin Health Analysis",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables BEFORE importing config
from dotenv import load_dotenv
load_dotenv()

# Now import modules that depend on environment variables
from src.config import config
from src.image_handler import ImageHandler
from src.ai_analyzer import analyzer
from src.utils import (
    setup_logging,
    display_error,
    display_success,
    display_info,
    display_warning
)

# Setup logging
setup_logging()

# Custom CSS for better mobile responsiveness and styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B9D;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #E55A8C;
        border: none;
    }
    .upload-container {
        border: 2px dashed #FF6B9D;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #FFF5F8;
    }
    .info-box {
        background-color: #F0F2F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    h1 {
        color: #FF6B9D;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


def render_header():
    """Render the application header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("✨ Jild AI")
        st.markdown("**Your Personal AI Skin Health Analyst**")
    with col2:
        st.image("https://img.icons8.com/?size=100&id=hNQmSdQgwUx2&format=png&color=000000", width=100)
    
    st.markdown("---")


def render_sidebar():
    """Render the sidebar with instructions and configuration."""
    with st.sidebar:
        st.header("📋 How It Works")
        st.markdown("""
        1. **Upload** a clear photo of your skin
        2. **Analyze** to get insights
        3. **Review** personalized recommendations
        """)

        # Settings section - Commented out for now
        # st.markdown("---")
        # st.header("⚙️ Settings")
        # # API Configuration Status
        # st.subheader("API Status")
        # if config.is_openrouter_configured():
        #     st.success("✅ OpenRouter Connected")
        # else:
        #     st.warning("⚠️ OpenRouter Not Configured")
        # if config.is_huggingface_configured():
        #     st.success("✅ Hugging Face Connected")
        # else:
        #     st.warning("⚠️ Hugging Face Not Configured")
        # st.markdown("---")

        st.markdown("---")

        # Tips
        st.header("💡 Tips for Best Results")
        st.markdown("""
        - Use **natural lighting**
        - Take **close-up** photos
        - Keep the image **in focus**
        - **Clean** skin before photos
        - Avoid **filters**
        """)
        
        st.markdown("---")
        
        # Disclaimer
        st.caption("""
        **Disclaimer:** This app provides general skincare guidance only. 
        For medical concerns, please consult a licensed dermatologist.
        """)


def render_api_setup_guide():
    """Render setup guide if no APIs are configured."""
    st.warning("⚠️ No API keys configured. Please set up at least one API to use the app.")
    
    with st.expander("🔧 Setup Instructions", expanded=True):
        st.markdown("""
        ### For Local Development:
        
        1. Create a `.env` file in the project root
        2. Add your API keys:
        ```
        OPENROUTER_API_KEY=your_key_here
        HUGGINGFACE_API_KEY=your_key_here
        ```
        
        ### For Streamlit Cloud:
        
        1. Go to your app settings
        2. Navigate to "Secrets"
        3. Add your API keys:
        ```toml
        OPENROUTER_API_KEY = "your_key_here"
        HUGGINGFACE_API_KEY = "your_key_here"
        ```
        
        ### Getting API Keys:
        
        - **OpenRouter**: Visit [openrouter.ai](https://openrouter.ai) to get your API key
        - **Hugging Face**: Visit [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) to create a token
        """)


def main():
    """Main application function."""
    render_header()
    render_sidebar()
    
    # Check if any API is configured
    if not config.is_openrouter_configured() and not config.is_huggingface_configured():
        st.warning("⚠️ No API keys configured. Please set up at least one API to use the app.")
        #render_api_setup_guide()
        return
    
    # Get available models
    available_models = config.get_available_models()
    
    if not available_models:
        display_error("No models available. Please configure at least one API key.")
        return
    
    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.header("📸 Upload Your Skin Image")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=config.supported_formats,
            help="Upload a clear photo of the skin area you want to analyze",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            result = ImageHandler.prepare_image_for_api(uploaded_file)
            
            if result is not None:
                image, base64_image = result
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Display image info
                img_info = ImageHandler.get_image_info(image)
                st.caption(f"📐 Size: {img_info['width']}x{img_info['height']} pixels")
                
                # Store in session state
                st.session_state['image'] = image
                st.session_state['base64_image'] = base64_image
    
    with col2:
        st.header("🤖 AI Analysis")

        # Hardcoded model selection - using Qwen as a wrapper for now
        # TODO: Replace with custom model in the future
        selected_model_name = "🔒 Qwen2.5"
        selected_model_id = "qwen/qwen2.5-vl-32b-instruct:free"

        # # Model selection dropdown (commented out - will use custom model later)
        # selected_model_name = st.selectbox(
        #     "Select AI Model",
        #     options=list(available_models.keys()),
        #     help="Choose the AI model for analyzing your skin"
        # )
        # selected_model_id = available_models[selected_model_name]

        # Display model info
        st.caption(f"Powered by Jild AI Vision Model")

        # Analyze button
        analyze_button = st.button("🔍 Analyze My Skin", type="primary")

        if analyze_button:
            if 'base64_image' not in st.session_state:
                display_error("Please upload an image first!")
            else:
                with st.spinner("🧬 Analyzing your skin... This may take a moment..."):
                    # Perform analysis
                    result = analyzer.analyze_skin(
                        st.session_state['base64_image'],
                        selected_model_name,
                        selected_model_id
                    )

                    # Store result in session state
                    st.session_state['analysis_result'] = result
    
    # Display results
    if 'analysis_result' in st.session_state:
        st.markdown("---")
        
        result = st.session_state['analysis_result']
        
        if result['success']:
            st.header("📊 Analysis Results")
            
            # Display provider info
            col_a, col_b = st.columns([3, 1])
            with col_a:
                #st.caption(f"Powered by: {result['provider']} - {result['model']}")
                st.caption(f"Powered by Jild AI Vision Model")
            with col_b:
                if st.button("🔄 Clear Results"):
                    del st.session_state['analysis_result']
                    st.rerun()
            
            # Display analysis
            st.markdown(result['analysis'])
            
            display_success("Analysis completed successfully!")
            
            # Download option
            st.download_button(
                label="📥 Download Report",
                data=result['analysis'],
                file_name="skincare_analysis.md",
                mime="text/markdown"
            )
        else:
            display_error(f"Analysis failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()

