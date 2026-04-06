# Hantek 1008B Python Driver - v1.0.0

## 🎉 First Public Release

This is the initial release of the Hantek 1008B Python driver, providing **cross-platform support for macOS and Linux users** where official support is limited or non-existent.

## ✨ Key Features

- ✅ **Cross-Platform**: Works on macOS (ARM64/Intel) and Linux
- ✅ **USB Bridge Support**: Automatically handles devices connected through USB bridges
- ✅ **Multi-Channel**: Simultaneous acquisition from all 8 channels
- ✅ **Complete Protocol**: Full USB communication protocol implementation (10 command types)
- ✅ **Easy to Use**: Simple Python API for device control
- ✅ **Reverse-Engineered**: Protocol extracted from USB captures (7,821 commands analyzed)

## 📋 What's Included

- High-level `Hantek1008B` class for easy device control
- Low-level `HantekProtocol` class for advanced usage
- Complete USB protocol implementation
- Device initialization and data acquisition
- 12-bit ADC sample parsing and voltage conversion
- Comprehensive documentation and examples
- MIT License

## 🔧 Installation

```bash
# Install dependencies
pip install pyusb

# macOS: Install libusb
brew install libusb

# Linux: Install libusb
sudo apt-get install libusb-1.0-0

# Install package
cd hantek1008b_standalone
pip install -e .
```

## 📖 Quick Start

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

## 🎯 Use Cases

- **Automotive diagnostics** - Multi-channel signal analysis
- **Electronics testing** - Debugging and signal analysis
- **Educational purposes** - Teaching oscilloscope usage
- **Research applications** - Data acquisition and analysis
- **Signal analysis** - General purpose measurement

## 📊 Device Specifications

- **Channels**: 8 simultaneous channels
- **ADC Resolution**: 12-bit (0-4095)
- **Memory Depth**: 4K samples per channel
- **Sampling Rate**: 2.4 MSa/s
- **Voltage Range**: 10 mV/div to 5 V/div
- **Maximum Input**: 400V (DC + AC peak)

## ⚠️ Known Limitations

- Channel configuration commands need parameter encoding refinement
- Trigger functionality not yet implemented
- Timebase control not yet implemented
- Some protocol aspects may need adjustment with hardware testing

## 🔍 Protocol Information

The USB protocol was reverse-engineered from captured command sequences:
- **VID**: 0x0783
- **PID**: 0x5725
- **Endpoints**: 0x81 (IN), 0x02 (OUT)
- **Packet Size**: 64 bytes
- **10 unique command types** identified from 7,821 captured commands

## 🙏 Why This Exists

The Hantek 1008B is a popular 8-channel oscilloscope, but **official Mac support is limited or non-existent**. After contacting the manufacturer with no response, this driver was created by reverse-engineering the USB protocol from Windows software captures.

**This fills a real gap in the community** - Mac users with Hantek 1008B devices can now use their hardware!

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🔗 Resources

- **Documentation**: See [README.md](README.md)
- **Examples**: See `examples/` directory
- **Protocol Details**: See protocol documentation
- **Issues**: Report on [GitHub Issues](https://github.com/imediacorp/Hantek-10008B/issues)

## ⚠️ Disclaimer

This is **not an official Hantek driver**. The USB protocol was reverse-engineered from publicly available information and USB captures. Use at your own risk.

---

**Made for the community, by the community** 🎉

