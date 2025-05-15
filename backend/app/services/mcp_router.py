from typing import Dict, Any, Optional
import aiohttp
from app.core.config import settings
import json

class MCPRouter:
    """Model Coordination Protocol Router for managing multiple AI model providers"""
    
    def __init__(self):
        self.providers = {
            "openai": {
                "api_key": settings.OPENAI_API_KEY,
                "base_url": "https://api.openai.com/v1"
            },
            "google": {
                "api_key": settings.GOOGLE_API_KEY,
                "base_url": "https://generativelanguage.googleapis.com/v1"
            },
            "anthropic": {
                "api_key": settings.ANTHROPIC_API_KEY,
                "base_url": "https://api.anthropic.com/v1"
            },
            "deepseek": {
                "api_key": settings.DEEPSEEK_API_KEY,
                "base_url": "https://api.deepseek.com/v1"
            }
        }

    async def route_request(
        self,
        query: str,
        provider: str = "openai",
        model_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Route the request to appropriate AI provider"""
        if provider not in self.providers:
            raise ValueError(f"Unsupported provider: {provider}")

        if not self.providers[provider]["api_key"]:
            raise ValueError(f"API key not configured for provider: {provider}")

        try:
            response = await self._make_api_request(
                provider=provider,
                query=query,
                model_params=model_params or {}
            )
            return response

        except Exception as e:
            print(f"Error routing request to {provider}: {str(e)}")
            # Try fallback provider if primary fails
            if provider != "openai":
                print("Attempting fallback to OpenAI...")
                return await self.route_request(query, "openai", model_params)
            raise

    async def _make_api_request(
        self,
        provider: str,
        query: str,
        model_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make API request to the specified provider"""
        provider_config = self.providers[provider]
        headers = {
            "Authorization": f"Bearer {provider_config['api_key']}",
            "Content-Type": "application/json"
        }

        # Prepare request based on provider
        if provider == "openai":
            endpoint = f"{provider_config['base_url']}/chat/completions"
            payload = {
                "model": model_params.get("model", "gpt-4"),
                "messages": [{"role": "user", "content": query}],
                "temperature": model_params.get("temperature", 0.7),
                "max_tokens": model_params.get("max_tokens", 1000)
            }
        elif provider == "anthropic":
            endpoint = f"{provider_config['base_url']}/messages"
            payload = {
                "model": model_params.get("model", "claude-3-opus"),
                "messages": [{"role": "user", "content": query}],
                "max_tokens": model_params.get("max_tokens", 1000)
            }
        # Add other provider implementations as needed

        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"API request failed: {await response.text()}")
                return await response.json()

    def get_provider_status(self, provider: str) -> Dict[str, Any]:
        """Get the status and capabilities of a provider"""
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")

        return {
            "available": bool(self.providers[provider]["api_key"]),
            "capabilities": self._get_provider_capabilities(provider)
        }

    def _get_provider_capabilities(self, provider: str) -> Dict[str, Any]:
        """Get the capabilities of a specific provider"""
        capabilities = {
            "openai": {
                "models": ["gpt-4", "gpt-3.5-turbo"],
                "features": ["chat", "function-calling", "vision"]
            },
            "anthropic": {
                "models": ["claude-3-opus", "claude-3-sonnet"],
                "features": ["chat", "analysis"]
            },
            # Add other provider capabilities
        }
        return capabilities.get(provider, {})
