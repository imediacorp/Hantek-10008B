# Contributing to Hantek 1008B Python Driver

Thank you for your interest in contributing! This project welcomes contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:
1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear description of the problem/feature
   - Steps to reproduce (for bugs)
   - System information (OS, Python version, libusb version)
   - Error messages or logs

### Contributing Code

1. **Fork the repository**
2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code style
4. **Test your changes**:
   ```bash
   python -m pytest  # If tests exist
   python examples/basic_usage.py  # Test with actual device
   ```
5. **Commit your changes** with clear messages
6. **Push to your fork** and create a Pull Request

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

### Areas for Contribution

- **Channel Configuration**: Implement voltage range, coupling settings
- **Trigger Functionality**: Add trigger control and settings
- **Timebase Control**: Implement timebase configuration
- **Performance**: Optimize data acquisition for large sample counts
- **Documentation**: Improve examples, add tutorials
- **Testing**: Add unit tests and integration tests
- **Protocol Refinement**: Help refine protocol based on hardware testing

### Testing

If you have a Hantek 1008B device:
- Test your changes with actual hardware
- Report any protocol issues or improvements
- Share test results and findings

### Questions?

Feel free to open an issue for questions or discussions about contributions.

Thank you for helping make this driver better for the community!

