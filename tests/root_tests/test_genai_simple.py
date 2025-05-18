import os
import toml
from google import genai

def test_genai_directly(api_key=None):
    """
    Test the Google Gen AI SDK directly.
    
    Args:
        api_key: Optional API key to use. If not provided, will try to get from environment or .secrets.toml.
    """
    # Get the API key from environment variable, parameter, or .secrets.toml
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # If not in environment, try to get from .secrets.toml
        if not api_key:
            secrets_path = os.path.join(
                os.path.dirname(__file__), 
                "alpha_codium", 
                "settings", 
                ".secrets.toml"
            )
            
            if os.path.exists(secrets_path):
                try:
                    with open(secrets_path, "r") as f:
                        config = toml.load(f)
                        if "gemini" in config and "key" in config["gemini"]:
                            api_key = config["gemini"]["key"]
                            print("Using API key from .secrets.toml")
                except Exception as e:
                    print(f"Error reading .secrets.toml: {e}")
            
            if not api_key:
                print("No API key provided. Please set the GEMINI_API_KEY environment variable, pass the key as an argument, or add it to .secrets.toml.")
                return
    
    print(f"Testing Google Gen AI SDK with key: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    
    # Create a client
    client = genai.Client(api_key=api_key)
    
    # Generate content
    prompt = "Write a simple Python function to calculate the factorial of a number."
    print(f"Sending prompt: {prompt}")
    
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",  # Using flash model which might have a higher quota
            contents=prompt,
            config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 0,
                "max_output_tokens": 8192,
                "system_instruction": "You are a helpful coding assistant."
            }
        )
        
        # Print the response
        print("\nResponse from Gemini:")
        print("-" * 50)
        print(response.text)
        print("-" * 50)
        print("Test completed successfully!")
        return True
    except Exception as e:
        print(f"Error during Gemini API test: {e}")
        return False

if __name__ == "__main__":
    test_genai_directly()