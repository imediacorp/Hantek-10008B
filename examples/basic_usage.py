#!/usr/bin/env python3
"""Basic usage example for Hantek 1008B driver."""

from hantek1008b import Hantek1008B

def main():
    # Create scope instance
    scope = Hantek1008B()
    
    # Connect to device
    print("Connecting to Hantek 1008B...")
    if not scope.connect():
        print("❌ Device not found")
        print("   Make sure the device is connected and powered on")
        return 1
    
    print("✅ Device connected")
    
    # Initialize
    print("Initializing device...")
    if scope.initialize():
        print("✅ Device initialized")
    else:
        print("⚠️  Initialization returned False (may be normal)")
    
    # Read data from channels 1-2
    print("\nReading data from channels 1-2 (512 samples each)...")
    data = scope.read_channels([1, 2], samples=512, voltage_range=5.0)
    
    if data:
        print(f"✅ Successfully read data from {len(data)} channel(s)")
        for ch, voltages in data.items():
            print(f"\nChannel {ch}:")
            print(f"  Samples: {len(voltages)}")
            if voltages:
                print(f"  Min: {min(voltages):.3f}V")
                print(f"  Max: {max(voltages):.3f}V")
                print(f"  Mean: {sum(voltages)/len(voltages):.3f}V")
    else:
        print("❌ Failed to read data")
    
    # Disconnect
    scope.disconnect()
    print("\n✅ Disconnected")
    
    return 0

if __name__ == "__main__":
    exit(main())

