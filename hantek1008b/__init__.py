"""
Hantek 1008B Python Driver

A standalone Python library for controlling the Hantek 1008B 8-channel USB oscilloscope
on macOS and Linux platforms.

Example:
    from hantek1008b import Hantek1008B
    
    scope = Hantek1008B()
    if scope.connect():
        scope.initialize()
        data = scope.read_channels([1, 2], samples=1024)
        print(f"Channel 1: {len(data[1])} samples")
"""

from .device import Hantek1008B
from .protocol import HantekCommands, HantekProtocol

__version__ = "1.0.0"
__all__ = ["Hantek1008B", "HantekCommands", "HantekProtocol"]

