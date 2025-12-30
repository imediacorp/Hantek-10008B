# Release Notes - v1.0.0

## Hantek 1008B Python Driver - Initial Release

### 🎉 First Public Release

This is the initial release of the Hantek 1008B Python driver, providing cross-platform support for macOS and Linux users.

### ✨ Key Features

- **Cross-Platform**: Works on macOS (ARM64/Intel) and Linux
- **USB Bridge Support**: Automatically handles devices connected through USB bridges
- **Multi-Channel**: Simultaneous acquisition from all 8 channels
- **Complete Protocol**: Full USB communication protocol implementation
- **Easy to Use**: Simple Python API

### 📋 What's Included

- High-level `Hantek1008B` class for easy device control
- Low-level `HantekProtocol` class for advanced usage
- Complete USB protocol implementation (10 command types)
- Device initialization and data acquisition
- 12-bit ADC sample parsing and voltage conversion
- Comprehensive documentation and examples

### 🔧 Installation

```bash
# Install dependencies
pip install pyusb

# macOS: Install libusb
brew install libusb

# Linux: Install libusb
sudo apt-get install libusb-1.0-0

# Install package
pip install hantek1008b
```

### 📖 Quick Start

```python
from hantek1008b import Hantek1008B

scope = Hantek1008B()
if scope.connect():
    scope.initialize()
    data = scope.read_channels([1, 2], samples=1024)
    print(f"Channel 1: {len(data[1])} samples")
```

### 🎯 Use Cases

- Automotive diagnostics
- Electronics testing and debugging
- Educational purposes
- Research applications
- Signal analysis

### ⚠️ Known Limitations

- Channel configuration commands need parameter encoding refinement
- Trigger functionality not yet implemented
- Timebase control not yet implemented
- Some protocol aspects may need adjustment with hardware testing

### 🙏 Acknowledgments

This driver was created by reverse-engineering the USB protocol from captured command sequences. Special thanks to the community for the need that drove this development.

### 📝 License

MIT License - See LICENSE file for details

### 🔗 Resources

- Documentation: See README.md
- Examples: See examples/ directory
- Protocol Details: See protocol documentation
- Issues: Report on GitHub Issues

---

**Made for the community, by the community** 🎉

