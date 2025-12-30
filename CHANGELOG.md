# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-30

### Added
- Initial release of Hantek 1008B Python driver
- Cross-platform support (macOS ARM64/Intel, Linux)
- USB bridge support for devices connected through USB bridges
- Multi-channel simultaneous data acquisition (up to 8 channels)
- 12-bit ADC sample parsing and voltage conversion
- Complete USB protocol implementation (10 command types)
- Device initialization sequence
- High-level `Hantek1008B` API class
- Low-level `HantekProtocol` class for advanced usage
- Context manager support for automatic cleanup
- Comprehensive documentation and examples
- MIT License for open source distribution

### Technical Details
- Reverse-engineered USB protocol from captured command sequences
- Protocol based on 7,821 captured commands with 10 unique types
- Supports 4K samples per channel (device maximum)
- 2.4 MSa/s sampling rate capability
- Automatic backend detection for libusb (handles ARM64/Intel differences)

### Known Limitations
- Channel configuration commands identified but parameter encoding needs refinement
- Trigger functionality not yet implemented
- Timebase control not yet implemented
- Some protocol aspects based on hypotheses and may need adjustment with hardware testing

[1.0.0]: https://github.com/yourusername/hantek1008b/releases/tag/v1.0.0

