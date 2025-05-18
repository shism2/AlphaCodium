import logging
from typing import Tuple, Optional
import asyncio

from google import genai
from aiolimiter import AsyncLimiter
from retry import retry

from alpha_codium.settings.config_loader import get_settings
from alpha_codium.log import get_logger

logger = get_logger(__name__)
GEMINI_RETRIES = 5


class GeminiHandler:
    """
    This class handles interactions with the Google Gemini API for chat completions.
    It initializes the API key and other settings from a configuration file,
    and provides a method for performing chat completions using the Gemini API.
    """

    def __init__(self):
        """
        Initializes the Gemini API key and other settings from a configuration file.
        Raises a ValueError if the Gemini key is missing.
        """
        self.limiter = AsyncLimiter(get_settings().config.max_requests_per_minute)
        try:
            self.client = genai.Client(api_key=get_settings().gemini.key)
        except AttributeError as e:
            raise ValueError("Gemini API key is required") from e

    @retry(
        exceptions=(Exception,),
        tries=GEMINI_RETRIES,
        delay=2,
        backoff=2,
        jitter=(1, 3),
    )
    async def chat_completion(
            self, model: str,
            system: str,
            user: str,
            temperature: float = 0.2,
            frequency_penalty: float = 0.0,
    ) -> Tuple[str, Optional[str]]:
        """
        Performs a chat completion using the Gemini API.
        
        Args:
            model: The model to use for the completion
            system: The system message
            user: The user message
            temperature: The temperature to use for the completion
            frequency_penalty: The frequency penalty to use for the completion
            
        Returns:
            A tuple containing the response text and the finish reason
        """
        try:
            logger.info("-----------------")
            logger.info("Running inference with Gemini...")
            logger.debug(f"system:\n{system}")
            logger.debug(f"user:\n{user}")
            
            # Map model names from OpenAI to Gemini
            gemini_model = self._map_model_name(model)
            
            # Run the generation in a thread to make it async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: self.client.models.generate_content(
                model=gemini_model,
                contents=user,
                config={
                    "temperature": temperature,
                    "top_p": 0.95,
                    "top_k": 0,
                    "max_output_tokens": 8192,
                    "system_instruction": system
                }
            ))
            
            # Get the response text
            resp = response.text
            
            # Gemini doesn't provide a finish reason, so we'll use None
            finish_reason = None
            
            logger.debug(f"response:\n{resp}")
            logger.info('done')
            logger.info("-----------------")
            return resp, finish_reason
            
        except Exception as e:
            logging.error(f"Error during Gemini inference: {e}")
            raise

    def _map_model_name(self, model_name: str) -> str:
        """
        Maps model names to Gemini model names.
        Only includes Gemini 2.0 models and above.
        
        Args:
            model_name: The model name
            
        Returns:
            The corresponding Gemini model name
        """
        model_mapping = {
            "gemini-2.0-pro": "models/gemini-2.0-pro-exp",
            "gemini-2.0-flash": "models/gemini-2.0-flash",
        }
        
        # Use the mapping if available, otherwise use the default model
        return model_mapping.get(model_name, "models/gemini-2.0-flash")