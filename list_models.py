#!/usr/bin/env python3
"""
Script to list available Gemini models.
"""

import os
import sys
import logging
import google.generativeai as genai
from alpha_codium.settings.config_loader import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def get_api_key():
    """Get the Gemini API key from settings or environment."""
    # Try to read directly from the .secrets.toml file
    import toml
    try:
        # Find all .secrets.toml files
        import subprocess
        result = subprocess.run(
            ["find", ".", "-name", ".secrets.toml", "-type", "f"], 
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True, 
            text=True
        )
        
        if result.stdout:
            # Use the first .secrets.toml file found
            secrets_path = result.stdout.strip().split('\n')[0]
            secrets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), secrets_path)
            
            if os.path.exists(secrets_path):
                secrets = toml.load(secrets_path)
                # Check for key in different formats
                if "gemini" in secrets and "key" in secrets["gemini"]:
                    return secrets["gemini"]["key"]
                elif "gemini_api_key" in secrets:
                    return secrets["gemini_api_key"]
    except Exception as e:
        logger.error(f"Error reading .secrets.toml: {e}")
    
    # If not in settings, try environment variable
    api_key = os.environ.get("GEMINI_API_KEY", None)
    
    return api_key

def list_available_models():
    """List all available Gemini models."""
    api_key = get_api_key()
    
    if not api_key:
        logger.error("No Gemini API key found. Please set it in .secrets.toml or as GEMINI_API_KEY environment variable.")
        return
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    try:
        # List available models
        models = genai.list_models()
        
        logger.info("Available Gemini models:")
        for model in models:
            if "gemini" in model.name.lower():
                logger.info(f"- {model.name}")
                logger.info(f"  Supported generation methods: {', '.join(model.supported_generation_methods)}")
                logger.info(f"  Display name: {model.display_name}")
                logger.info(f"  Description: {model.description}")
                logger.info(f"  Input token limit: {model.input_token_limit}")
                logger.info(f"  Output token limit: {model.output_token_limit}")
                logger.info("  ---")
    
    except Exception as e:
        logger.error(f"Error listing models: {e}")

if __name__ == "__main__":
    list_available_models()