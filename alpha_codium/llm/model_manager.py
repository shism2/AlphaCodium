"""
Model Manager for Gemini API

This module provides functionality to retrieve, cache, and manage available models
from the Gemini API.
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

from google import genai
from alpha_codium.log import get_logger
from alpha_codium.settings.config_loader import get_settings

class ModelManager:
    """
    A class to manage Gemini models, including retrieving available models,
    caching them locally, and providing model selection functionality.
    """
    
    def __init__(self, cache_dir: Optional[str] = None, cache_ttl: int = 86400):
        """
        Initialize the ModelManager.
        
        Args:
            cache_dir: Directory to store the model cache. If None, uses ~/.cache/alpha_codium
            cache_ttl: Time-to-live for the cache in seconds (default: 24 hours)
        """
        self.logger = get_logger(__name__)
        
        # Set up cache directory
        if cache_dir is None:
            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, ".cache", "alpha_codium")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "gemini_models.json"
        self.cache_ttl = cache_ttl
        
        # Initialize Gemini client
        try:
            self.client = genai.Client(api_key=get_settings().gemini.key)
        except AttributeError as e:
            self.logger.error("Gemini API key is required")
            self.client = None
    
    def get_available_models(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get a list of available Gemini models.
        
        Args:
            force_refresh: If True, bypass the cache and fetch fresh data
            
        Returns:
            A list of model information dictionaries
        """
        # Check if we have a valid cached response
        if not force_refresh and self._is_cache_valid():
            return self._load_from_cache()
        
        # If no client, return empty list
        if self.client is None:
            self.logger.error("Gemini client not initialized. Check API key.")
            return []
        
        try:
            # Fetch models from the API
            models = self._fetch_models_from_api()
            
            # Cache the results
            self._save_to_cache(models)
            
            return models
        except Exception as e:
            self.logger.error(f"Error fetching models: {e}")
            
            # If cache exists but is expired, use it as fallback
            if self.cache_file.exists():
                self.logger.info("Using expired cache as fallback")
                return self._load_from_cache()
            
            return []
    
    def _fetch_models_from_api(self) -> List[Dict[str, Any]]:
        """
        Fetch models directly from the Gemini API.
        
        Returns:
            A list of model information dictionaries
        """
        # Get all available models
        all_models = self.client.list_models()
        
        # Filter for Gemini models and format the response
        gemini_models = []
        for model in all_models:
            model_data = model.to_dict()
            if "gemini" in model_data.get("name", "").lower():
                # Extract relevant information
                model_info = {
                    "id": model_data.get("name", ""),
                    "display_name": self._get_display_name(model_data.get("name", "")),
                    "description": model_data.get("description", ""),
                    "input_token_limit": model_data.get("input_token_limit", 0),
                    "output_token_limit": model_data.get("output_token_limit", 0),
                    "supported_generation_methods": model_data.get("supported_generation_methods", []),
                }
                gemini_models.append(model_info)
        
        return gemini_models
    
    def _get_display_name(self, model_id: str) -> str:
        """
        Convert a model ID to a user-friendly display name.
        
        Args:
            model_id: The model ID (e.g., "models/gemini-1.5-pro")
            
        Returns:
            A user-friendly display name (e.g., "Gemini 1.5 Pro")
        """
        # Remove "models/" prefix if present
        if model_id.startswith("models/"):
            model_id = model_id[7:]
        
        # Split by hyphens and capitalize each part
        parts = model_id.split("-")
        
        # Handle special cases
        if len(parts) >= 3:
            # Format version numbers
            if parts[1].replace(".", "").isdigit():
                version = parts[1]
                model_type = " ".join(part.capitalize() for part in parts[2:])
                return f"{parts[0].capitalize()} {version} {model_type}"
        
        # Default formatting
        return " ".join(part.capitalize() for part in parts)
    
    def _is_cache_valid(self) -> bool:
        """
        Check if the cache file exists and is not expired.
        
        Returns:
            True if the cache is valid, False otherwise
        """
        if not self.cache_file.exists():
            return False
        
        # Check if the cache is expired
        cache_age = time.time() - self.cache_file.stat().st_mtime
        return cache_age < self.cache_ttl
    
    def _load_from_cache(self) -> List[Dict[str, Any]]:
        """
        Load models from the cache file.
        
        Returns:
            A list of model information dictionaries
        """
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            return cache_data.get("models", [])
        except Exception as e:
            self.logger.error(f"Error loading from cache: {e}")
            return []
    
    def _save_to_cache(self, models: List[Dict[str, Any]]) -> None:
        """
        Save models to the cache file.
        
        Args:
            models: A list of model information dictionaries
        """
        try:
            cache_data = {
                "timestamp": time.time(),
                "models": models
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
            self.logger.info(f"Saved {len(models)} models to cache")
        except Exception as e:
            self.logger.error(f"Error saving to cache: {e}")
    
    def get_recommended_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of recommended models for code generation.
        
        Returns:
            A list of recommended model information dictionaries
        """
        all_models = self.get_available_models()
        
        # Define priority models (newest and most capable first)
        priority_models = [
            "gemini-2.0-pro",
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro",
        ]
        
        # Filter and sort models based on priority
        recommended = []
        for priority_model in priority_models:
            for model in all_models:
                if priority_model in model["id"].lower():
                    recommended.append(model)
        
        # Add any other Gemini models not in the priority list
        for model in all_models:
            if not any(model["id"] == rec["id"] for rec in recommended):
                recommended.append(model)
        
        return recommended
    
    def get_model_by_id(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get model information by ID.
        
        Args:
            model_id: The model ID to look for
            
        Returns:
            The model information dictionary, or None if not found
        """
        models = self.get_available_models()
        
        # First try exact match
        for model in models:
            if model["id"] == model_id:
                return model
        
        # Then try partial match (without "models/" prefix)
        for model in models:
            if model_id in model["id"]:
                return model
        
        return None