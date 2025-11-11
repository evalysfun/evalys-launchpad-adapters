"""
Evalys Launchpad Adapters

Adapters for different memecoin launchpad platforms (Pump.fun, Bonk.fun, etc.)
"""

from .base_adapter import LaunchpadAdapter, CurveData, TokenInfo
from .pumpfun_adapter import PumpFunAdapter
from .bonkfun_adapter import BonkFunAdapter
from .generic_adapter import GenericAdapter

__all__ = [
    "LaunchpadAdapter",
    "CurveData",
    "TokenInfo",
    "PumpFunAdapter",
    "BonkFunAdapter",
    "GenericAdapter",
]

__version__ = "0.1.0"

