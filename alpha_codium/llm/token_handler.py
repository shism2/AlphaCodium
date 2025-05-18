from jinja2 import Environment, StrictUndefined

from alpha_codium.settings.config_loader import get_settings


class TokenHandler:
    """
    A class for handling tokens in the context of a pull request.

    Attributes:
    - prompt_tokens: The number of tokens in the system and user strings, as calculated by the _get_system_user_tokens
      method.
    """

    def __init__(self, message=None, vars: dict = {}, system="", user=""):  # noqa: B006
        """
        Initializes the TokenHandler object.

        Args:
        - message: The message object.
        - vars: A dictionary of variables.
        - system: The system string.
        - user: The user string.
        """
        if message is not None:
            self.prompt_tokens = self._get_system_user_tokens(
                message, vars, system, user
            )

    def _get_system_user_tokens(self, message, vars: dict, system, user):
        """
        Calculates the number of tokens in the system and user strings.
        For Gemini, we use a simple character count approximation.

        Args:
        - message: The message object.
        - vars: A dictionary of variables.
        - system: The system string.
        - user: The user string.

        Returns:
        The sum of the number of tokens in the system and user strings.
        """
        environment = Environment(undefined=StrictUndefined)
        system_prompt = environment.from_string(system).render(vars)
        user_prompt = environment.from_string(user).render(vars)
        
        # Simple approximation: 1 token ≈ 4 characters
        system_prompt_tokens = len(system_prompt) // 4
        user_prompt_tokens = len(user_prompt) // 4
        
        return system_prompt_tokens + user_prompt_tokens

    def count_tokens(self, patch: str) -> int:
        """
        Counts the number of tokens in a given patch string.
        For Gemini, we use a simple character count approximation.

        Args:
        - patch: The patch string.

        Returns:
        The number of tokens in the patch string.
        """
        # Simple approximation: 1 token ≈ 4 characters
        return len(patch) // 4
