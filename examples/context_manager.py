#!/usr/bin/env python3
"""Example using context manager for automatic cleanup."""

from hantek1008b import Hantek1008B

# Using context manager (automatic disconnect)
with Hantek1008B() as scope:
    if scope.connect():
        scope.initialize()
        data = scope.read_channels([1, 2, 3, 4], samples=1024)
        
        for ch, voltages in data.items():
            print(f"Channel {ch}: {len(voltages)} samples")
    
    # Automatically disconnected when exiting 'with' block

