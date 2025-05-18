#!/usr/bin/env python3
"""
Setup script for Google Gemini integration with AlphaCodium.
This script helps users set up their Gemini API key and configuration.
"""

import os
import sys

# Add the parent directory to the path so we can import from alpha_codium
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Print environment information for debugging
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Script path: {__file__}")
print(f"sys.path: {sys.path}")

try:
    import toml
    print(f"toml version: {toml.__version__}")
except ImportError:
    print("The 'toml' package is required but not installed.")
    print("Installing it now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "toml"])
    import toml
    print("Successfully installed 'toml' package.")

def setup_gemini_api_key():
    """
    Set up the Gemini API key in the .secrets.toml file.
    """
    print("=" * 50)
    print("Google Gemini Setup for AlphaCodium")
    print("=" * 50)
    
    # Path to the .secrets.toml file
    secrets_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "alpha_codium", 
        "settings", 
        ".secrets.toml"
    )
    
    # Check if the API key is already set
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, "r") as f:
                config = toml.load(f)
                if "gemini" in config and "key" in config["gemini"] and config["gemini"]["key"]:
                    print(f"\nGemini API key is already set in {secrets_path}")
                    api_key = config["gemini"]["key"]
                    print(f"Using existing API key: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
                    return True
        except Exception as e:
            print(f"Error reading existing secrets file: {e}")
    
    print("\nThis script will help you set up your Google Gemini API key.")
    print("You can get your API key from: https://makersuite.google.com/app/apikey\n")
    
    # Get the API key from the user
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("Error: API key cannot be empty.")
        return False
    
    # Create or update the .secrets.toml file
    try:
        # Check if the file exists
        if os.path.exists(secrets_path):
            # Load existing configuration
            with open(secrets_path, "r") as f:
                config = toml.load(f)
        else:
            config = {}
        
        # Add or update the Gemini section
        if "gemini" not in config:
            config["gemini"] = {}
        
        config["gemini"]["key"] = api_key
        
        # Write the updated configuration back to the file
        with open(secrets_path, "w") as f:
            toml.dump(config, f)
        
        print(f"\nGemini API key has been saved to {secrets_path}")
        
        # Update the configuration to use Gemini
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "alpha_codium", 
            "settings", 
            "configuration.toml"
        )
        
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    app_config = toml.load(f)
                
                # Check if the model is already set to a Gemini model
                current_model = app_config.get("config", {}).get("model", "")
                if not current_model.startswith("gemini-"):
                    # Ask if the user wants to switch to Gemini
                    switch = input("\nDo you want to set Gemini as the default model? (y/n): ").strip().lower()
                    if switch == "y":
                        if "config" not in app_config:
                            app_config["config"] = {}
                        
                        app_config["config"]["model"] = "gemini-1.5-pro"
                        
                        with open(config_path, "w") as f:
                            toml.dump(app_config, f)
                        print("Default model has been set to gemini-1.5-pro")
            except Exception as e:
                print(f"Warning: Could not update configuration file: {e}")
        
        # Test the API key
        print("\nTesting the Gemini API key...")
        try:
            from google import genai
            
            # Create a client
            client = genai.Client(api_key=api_key)
            
            # Generate content
            response = client.models.generate_content(
                model="gemini-1.5-flash",  # Using flash for quick test
                contents="Say hello in one word.",
                config={
                    "temperature": 0.2,
                    "max_output_tokens": 100,
                }
            )
            
            print(f"Test successful! Response: {response.text}")
        except Exception as e:
            print(f"Warning: Could not test the API key: {e}")
            print("You may need to check if the API key is valid.")
        
        print("\nSetup complete! You can now use AlphaCodium with Google Gemini models.")
        print("For more information, see GEMINI_INTEGRATION.md")
        return True
        
    except Exception as e:
        print(f"Error setting up Gemini API key: {e}")
        return False

if __name__ == "__main__":
    setup_gemini_api_key()