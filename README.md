# Hantek 1008B Python Driver for macOS/Linux

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/imediacorp/Hantek-10008B)
[![Release](https://img.shields.io/github/v/release/imediacorp/Hantek-10008B)](https://github.com/imediacorp/Hantek-10008B/releases)

A Python library for controlling the Hantek 1008B 8-channel USB oscilloscope on macOS and Linux. This driver was reverse-engineered from USB protocol captures and provides full control over the device.

> **Note**: This is not an official Hantek driver. The USB protocol was reverse-engineered from publicly available information and USB captures.

## Features

- ✅ **Cross-platform**: Works on macOS (ARM64/Intel) and Linux
- ✅ **USB Bridge Support**: Automatically handles devices connected through USB bridges
- ✅ **Multi-channel**: Simultaneous acquisition from all 8 channels
- ✅ **Full Protocol**: Complete implementation of USB communication protocol
- ✅ **Easy to Use**: Simple Python API for device control
- ✅ **No Dependencies**: Only requires pyusb and libusb

## Why This Exists

The Hantek 1008B is a popular 8-channel oscilloscope, but **official Mac support is limited or non-existent**. After contacting the manufacturer with no response, this driver was created by reverse-engineering the USB protocol from Windows software captures, making the device usable on macOS and Linux platforms.

**This fills a real gap in the community** - Mac users with Hantek 1008B devices can now use their hardware!

## Installation

### Prerequisites

**macOS (Apple Silicon):**
```bash
# Install libusb via Homebrew
/opt/homebrew/bin/brew install libusb

# Or for Intel Macs
brew install libusb
```

**Linux:**
```bash
sudo apt-get install libusb-1.0-0
# or
sudo yum install libusb
```

### Python Package

```bash
pip install pyusb
```

Then copy the `hantek1008b` directory to your project, or install it:

```bash
cd hantek1008b_standalone
pip install -e .
```

## Quick Start

```python
from hantek1008b import Hantek1008B

# Connect to device
scope = Hantek1008B()
if not scope.connect():
    print("Device not found")
    exit(1)

# Initialize
scope.initialize()

# Read data from channels 1-2
data = scope.read_channels([1, 2], samples=1024)

# Process data
for channel, voltages in data.items():
    print(f"Channel {channel}: {len(voltages)} samples")
    print(f"  Min: {min(voltages):.3f}V, Max: {max(voltages):.3f}V")
```

## API Reference

### `Hantek1008B`

Main class for device control.

#### `connect(backend=None) -> bool`
Connect to the Hantek 1008B device. Returns `True` if successful.

**Parameters:**
- `backend`: Optional USB backend (for custom libusb paths)

**Example:**
```python
scope = Hantek1008B()
if scope.connect():
    print("Connected!")
```

#### `initialize() -> bool`
Initialize the device. Must be called after connection.

#### `read_channels(channels, samples=4096, voltage_range=5.0, timeout=3000) -> dict`
Read data from specified channels.

**Parameters:**
- `channels`: List of channel numbers (1-8)
- `samples`: Number of samples per channel (max 4096)
- `voltage_range`: Full-scale voltage range in Volts (default: 5.0)
- `timeout`: USB timeout in milliseconds

**Returns:**
Dictionary mapping channel numbers to lists of voltage values.

**Example:**
```python
data = scope.read_channels([1, 2, 3, 4], samples=2048, voltage_range=10.0)
```

#### `send_command(command) -> bool`
Send a raw command to the device.

#### `read_response(size=64) -> bytes`
Read response from device.

## Device Specifications

- **Channels**: 8 simultaneous channels
- **ADC Resolution**: 12-bit (0-4095)
- **Memory Depth**: 4K samples per channel
- **Sampling Rate**: 2.4 MSa/s
- **Voltage Range**: 10 mV/div to 5 V/div
- **Maximum Input**: 400V (DC + AC peak)

## Protocol Information

The USB protocol was reverse-engineered from captured command sequences:
- **VID**: 0x0783
- **PID**: 0x5725
- **Endpoints**: 0x81 (IN), 0x02 (OUT)
- **Packet Size**: 64 bytes
- **10 unique command types** identified

See `PROTOCOL.md` for detailed protocol documentation.

## Troubleshooting

### Device Not Found

1. Ensure device is connected and powered on
2. Check USB bridge connection (supported automatically)
3. On Linux, you may need `sudo` or udev rules:

```bash
# Create udev rule
sudo nano /etc/udev/rules.d/99-hantek1008b.rules
```

Add:
```
SUBSYSTEM=="usb", ATTR{idVendor}=="0783", ATTR{idProduct}=="5725", MODE="0666"
```

Then:
```bash
sudo udevadm control --reload-rules
```

### USB Backend Issues (macOS)

If you get "No backend available":

1. Verify libusb is installed:
   ```bash
   file /opt/homebrew/opt/libusb/lib/libusb-1.0.dylib
   ```

2. Specify backend explicitly:
   ```python
   import usb.backend.libusb1
   backend = usb.backend.libusb1.get_backend(
       find_library=lambda x: "/opt/homebrew/opt/libusb/lib/libusb-1.0.dylib"
   )
   scope = Hantek1008B()
   scope.connect(backend=backend)
   ```

## Examples

### Basic Data Acquisition

```python
from hantek1008b import Hantek1008B
import matplotlib.pyplot as plt

scope = Hantek1008B()
if not scope.connect():
    print("Device not found")
    exit(1)

scope.initialize()

# Read from channel 1
data = scope.read_channels([1], samples=1024)

# Plot
plt.plot(data[1])
plt.xlabel("Sample")
plt.ylabel("Voltage (V)")
plt.title("Channel 1")
plt.show()
```

### Multi-Channel Acquisition

```python
scope = Hantek1008B()
scope.connect()
scope.initialize()

# Read all 8 channels
data = scope.read_channels([1, 2, 3, 4, 5, 6, 7, 8], samples=2048)

# Process each channel
for ch in range(1, 9):
    voltages = data[ch]
    print(f"Channel {ch}: {len(voltages)} samples")
    if voltages:
        print(f"  Range: {min(voltages):.3f}V to {max(voltages):.3f}V")
```

## License

This driver is provided as-is for educational and diagnostic purposes. The USB protocol was reverse-engineered from publicly available information and USB captures.

**Note**: This is not an official Hantek driver. Use at your own risk.

## Contributing

Contributions welcome! Areas for improvement:
- Channel configuration (voltage range, coupling)
- Trigger functionality
- Timebase control
- Performance optimization
- Additional protocol commands

## Acknowledgments

- Protocol reverse-engineered from USB captures
- Inspired by the need for Mac support
- Built for the diagnostic and measurement community

## Disclaimer

This software is provided "as is" without warranty. The authors are not affiliated with Hantek. Use at your own risk.

## Support

For issues, questions, or contributions:
- Open an issue on the [GitHub repository](https://github.com/imediacorp/Hantek-10008B/issues)
- Check protocol documentation for details
- Review examples in the `examples/` directory

## Latest Release

**v1.0.0** - [View Release](https://github.com/imediacorp/Hantek-10008B/releases/tag/v1.0.0)

First public release with full cross-platform support for macOS and Linux.

---

**Made for the community, by the community** 🎉

**Repository**: https://github.com/imediacorp/Hantek-10008B

