"""
Hantek 1008B Device Interface

High-level API for controlling the Hantek 1008B oscilloscope.
"""

from typing import Optional, Dict, List, Any
import os

try:
    import usb.core
    import usb.backend.libusb1
    _HAVE_USB = True
except ImportError:
    _HAVE_USB = False

from .protocol import HantekProtocol, HANTEK_VID, HANTEK_PID


class Hantek1008B:
    """
    Hantek 1008B 8-channel USB oscilloscope controller.
    
    Example:
        scope = Hantek1008B()
        if scope.connect():
            scope.initialize()
            data = scope.read_channels([1, 2], samples=1024)
    """
    
    def __init__(self, vid: int = HANTEK_VID, pid: int = HANTEK_PID):
        """
        Initialize Hantek controller.
        
        Args:
            vid: USB vendor ID (default: Hantek VID)
            pid: USB product ID (default: Hantek PID)
        """
        self.vid = vid
        self.pid = pid
        self.device: Optional[Any] = None
        self.protocol: Optional[HantekProtocol] = None
        self.backend: Optional[Any] = None
        self._setup_backend()
    
    def _setup_backend(self) -> None:
        """Set up USB backend (handles ARM64/Intel Mac differences)."""
        if not _HAVE_USB:
            return
        
        # Try common libusb paths
        libusb_paths = [
            "/opt/homebrew/opt/libusb/lib/libusb-1.0.dylib",  # ARM64 Mac
            "/opt/homebrew/lib/libusb-1.0.dylib",  # ARM64 Mac alternative
            "/usr/local/lib/libusb-1.0.dylib",  # Intel Mac
        ]
        
        for lib_path in libusb_paths:
            if os.path.exists(lib_path):
                try:
                    self.backend = usb.backend.libusb1.get_backend(
                        find_library=lambda x: lib_path
                    )
                    if self.backend:
                        break
                except Exception:
                    continue
        
        # Fallback to default backend
        if not self.backend:
            try:
                self.backend = usb.backend.libusb1.get_backend()
            except Exception:
                pass
    
    def connect(self, backend: Optional[Any] = None) -> bool:
        """
        Connect to Hantek 1008B device.
        
        Args:
            backend: Optional USB backend (overrides auto-detection)
            
        Returns:
            True if connected successfully, False otherwise
        """
        if not _HAVE_USB:
            return False
        
        if backend is not None:
            self.backend = backend
        
        try:
            kwargs = {"idVendor": self.vid, "idProduct": self.pid}
            if self.backend:
                kwargs["backend"] = self.backend
            
            self.device = usb.core.find(**kwargs)
            
            if self.device is None:
                return False
            
            # Set configuration
            try:
                self.device.set_configuration()
            except Exception:
                pass
            
            # Claim interface
            try:
                usb.util.claim_interface(self.device, 0)
            except Exception:
                # Try release and reclaim
                try:
                    usb.util.release_interface(self.device, 0)
                    usb.util.claim_interface(self.device, 0)
                except Exception:
                    pass
            
            # Initialize protocol handler
            self.protocol = HantekProtocol(self.device)
            
            return True
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """Disconnect from device."""
        if self.device:
            try:
                usb.util.release_interface(self.device, 0)
            except Exception:
                pass
            self.device = None
            self.protocol = None
    
    def initialize(self, timeout: int = 2000) -> bool:
        """
        Initialize device (must be called after connect).
        
        Args:
            timeout: USB timeout in milliseconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.protocol:
            return False
        
        return self.protocol.initialize(timeout)
    
    def read_channels(
        self,
        channels: List[int],
        samples: int = 4096,
        voltage_range: float = 5.0,
        timeout: int = 3000,
    ) -> Dict[int, List[float]]:
        """
        Read data from specified channels.
        
        Args:
            channels: List of channel numbers (1-8)
            samples: Number of samples per channel (max 4096)
            voltage_range: Full-scale voltage range in Volts (default: 5.0)
            timeout: USB timeout in milliseconds
            
        Returns:
            Dictionary mapping channel numbers to lists of voltage values
            
        Example:
            data = scope.read_channels([1, 2, 3], samples=1024)
            print(data[1])  # List of voltage values for channel 1
        """
        if not self.protocol:
            return {}
        
        # Validate channels
        valid_channels = [ch for ch in channels if 1 <= ch <= 8]
        if not valid_channels:
            return {}
        
        # Limit samples
        samples = min(samples, 4096)
        
        return self.protocol.read_channels(
            valid_channels,
            sample_count=samples,
            voltage_range=voltage_range,
            timeout=timeout,
        )
    
    def send_command(self, command: bytes, timeout: int = 1000) -> bool:
        """
        Send a raw command to the device.
        
        Args:
            command: Command bytes
            timeout: USB timeout in milliseconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.protocol:
            return False
        
        return self.protocol.send_command(command, timeout)
    
    def read_response(self, size: int = 64, timeout: int = 1000) -> Optional[bytes]:
        """
        Read response from device.
        
        Args:
            size: Number of bytes to read
            timeout: USB timeout in milliseconds
            
        Returns:
            Response bytes, or None on error
        """
        if not self.protocol:
            return None
        
        return self.protocol.read_response(size, timeout)
    
    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self.device is not None and self.protocol is not None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.disconnect()

