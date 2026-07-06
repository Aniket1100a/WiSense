"""ProviderFactory: return provider instances based on provider name.

Factory consults the `ProviderRegistry` so new providers can register
themselves without changing this code.
"""

from typing import Any, Dict, Optional

from app.providers.registry import ProviderRegistry


class ProviderFactory:
    @staticmethod
    def get(provider_name: str, sensor_info: Optional[Dict[str, Any]] = None):
        if not provider_name:
            return None
        cls = ProviderRegistry.get_provider_class(provider_name)
        if not cls:
            # also try common aliases
            alias = provider_name.lower()
            cls = ProviderRegistry.get_provider_class(alias)
        if not cls:
            return None
        return cls(sensor_info or {})
