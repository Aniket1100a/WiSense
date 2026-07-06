"""Provider abstraction package for WiSense.

This package contains provider base classes, the provider factory and registry,
and placeholder provider implementations for supported providers.
"""

from .factory import ProviderFactory
from .registry import ProviderRegistry

# Import provider implementations so they auto-register in the registry.
from .esp32 import provider as esp32_provider
from .laptop import provider as laptop_provider
from .usb import provider as usb_provider
from .dataset import provider as dataset_provider
from .simulator import provider as simulator_provider

__all__ = ["ProviderFactory", "ProviderRegistry"]
