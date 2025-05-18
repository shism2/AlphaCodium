import logging
from aiolimiter import AsyncLimiter
from retry import retry

from alpha_codium.settings.config_loader import get_settings
from alpha_codium.log import get_logger
from alpha_codium.llm.gemini_handler import GeminiHandler

logger = get_logger(__name__)
GEMINI_RETRIES = 5


class AiHandler:
    """
    This class handles interactions with the Google Gemini API for chat completions.
    It initializes the API key and other settings from a configuration file,
    and provides a method for performing chat completions using the Gemini API.
    """

    def __init__(self):
        """
        Initializes the API keys and other settings from a configuration file.
        Raises a ValueError if the required API key is missing.
        """
        self.limiter = AsyncLimiter(get_settings().config.max_requests_per_minute)
        self.model_provider = self._get_model_provider()
        
        try:
            if self.model_provider == "gemini":
                self.gemini_handler = GeminiHandler()
            else:
                raise ValueError(f"Unsupported model provider: {self.model_provider}")
        except AttributeError as e:
            raise ValueError("Gemini API key is required") from e

    def _get_model_provider(self):
        """
        Determines the model provider based on the model name in the configuration.
        
        Returns:
            The model provider name: 'gemini'
        """
        model = get_settings().get("config.model").lower()
        if "gemini" in model:
            return "gemini"
        else:
            # Default to Gemini if model provider can't be determined
            return "gemini"

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
    ):
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
        if get_settings().config.verbosity_level >= 2:
            logging.debug(f"Generating completion with {model}")
        
        # Use Gemini handler
        return await self.gemini_handler.chat_completion(
            model=model,
            system=system,
            user=user,
            temperature=temperature,
            frequency_penalty=frequency_penalty
        )
