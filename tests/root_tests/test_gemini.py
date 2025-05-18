import asyncio
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from alpha_codium.llm.ai_handler import AiHandler
from alpha_codium.settings.config_loader import get_settings


async def test_gemini_integration():
    """
    Test the Gemini integration by sending a simple prompt and printing the response.
    """
    print("Testing Gemini integration...")
    print(f"Using model: {get_settings().config.model}")
    
    handler = AiHandler()
    
    system_prompt = "You are a helpful coding assistant."
    user_prompt = "Write a simple Python function to calculate the factorial of a number."
    
    try:
        response, finish_reason = await handler.chat_completion(
            model=get_settings().config.model,
            system=system_prompt,
            user=user_prompt,
            temperature=0.2
        )
        
        print("\nResponse from model:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        print(f"Finish reason: {finish_reason}")
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_gemini_integration())