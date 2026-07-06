"""Provider registry for automatic provider registration.

Providers should register themselves by calling `register_provider(name, cls)`
or using the `@register_provider(name)` decorator.
"""

from typing import Callable, Dict, Optional, Type

ProviderClass = Type


class ProviderRegistry:
    _registry: Dict[str, ProviderClass] = {}

    @classmethod
    def register_provider(cls, name: str, provider_cls: ProviderClass) -> None:
        cls._registry[name] = provider_cls

    @classmethod
    def get_provider_class(cls, name: str) -> Optional[ProviderClass]:
        return cls._registry.get(name)

    @classmethod
    def all_providers(cls) -> Dict[str, ProviderClass]:
        return dict(cls._registry)


def register_provider(name: str) -> Callable[[ProviderClass], ProviderClass]:
    def _decorator(provider_cls: ProviderClass) -> ProviderClass:
        ProviderRegistry.register_provider(name, provider_cls)
        return provider_cls

    return _decorator
