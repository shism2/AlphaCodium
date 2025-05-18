import logging
import traceback
from typing import Callable, List

from alpha_codium.settings.config_loader import get_settings


async def send_inference(f: Callable):
    all_models = _get_all_models()
    # try each model until one is successful, otherwise raise exception
    for i, model in enumerate(all_models):
        try:
            return await f(model)
        except Exception:
            logging.warning(
                f"Failed to generate prediction with {model}: "
                f"{traceback.format_exc()}"
            )
            if i == len(all_models) - 1:  # If it's the last iteration
                raise  # Re-raise the last exception


def _get_all_models() -> List[str]:
    model = get_settings().config.model
    fallback_models = get_settings().config.fallback_models
    if not isinstance(fallback_models, list):
        fallback_models = [m.strip() for m in fallback_models.split(",")]
    all_models = [model] + fallback_models
    return all_models
