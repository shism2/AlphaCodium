import os
import sys
from google import genai

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_gemini_directly(api_key=None):
    """
    Test the Gemini API directly without using the AlphaCodium integration.
    This is useful for verifying that the API key and connection work correctly.
    
    Args:
        api_key: Optional API key to use. If not provided, will try to get from environment.
    """
    # Get the API key from environment variable or parameter
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("No API key provided. Please set the GEMINI_API_KEY environment variable or pass the key as an argument.")
            return
    
    print(f"Testing Gemini API with key: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    
    # Create a client
    client = genai.Client(api_key=api_key)
    
    # Generate content
    prompt = "Write a simple Python function to calculate the factorial of a number."
    print(f"Sending prompt: {prompt}")
    
    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",
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
    test_gemini_directly()