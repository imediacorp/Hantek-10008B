"""
Hantek 1008B Device Interface

High-level API for controlling the Hantek 1008B oscilloscope.
"""

import logging
import os
from typing import Optional, Dict, List, Any

try:
    import usb.core
    import usb.util
    import usb.backend.libusb1
    _HAVE_USB = True
    _USBError = usb.core.USBError
except ImportError:
    _HAVE_USB = False
    _USBError = Exception

from .protocol import HantekProtocol, HANTEK_VID, HANTEK_PID, HANTEK_PACKET_SIZE

logger = logging.getLogger(__name__)

# Expected USB device strings for identity verification (M1)
_EXPECTED_MANUFACTURER = "Hantek"
_EXPECTED_PRODUCT = "1008B"


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
            "/opt/homebrew/lib/libusb-1.0.dylib",             # ARM64 Mac alternative
            "/usr/local/lib/libusb-1.0.dylib",                # Intel Mac
        ]

        for lib_path in libusb_paths:
            if os.path.exists(lib_path):
                try:
                    # H3: bind lib_path at definition time to avoid late-binding closure bug
                    self.backend = usb.backend.libusb1.get_backend(
                        find_library=lambda x, p=lib_path: p
                    )
                    if self.backend:
                        break
                except _USBError as e:
                    logger.debug("Failed to load backend from %s: %s", lib_path, e)
                    continue

        # Fallback to default backend
        if not self.backend:
            try:
                self.backend = usb.backend.libusb1.get_backend()
            except _USBError as e:
                logger.warning("Failed to load default libusb backend: %s", e)

    def connect(self, backend: Optional[Any] = None, verify_identity: bool = True) -> bool:
        """
        Connect to Hantek 1008B device.

        Args:
            backend: Optional USB backend (overrides auto-detection)
            verify_identity: If True, verify manufacturer/product strings (M1)

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
                logger.debug("No device found with VID=0x%04X PID=0x%04X", self.vid, self.pid)
                return False

            # M1: Verify device identity beyond VID/PID to guard against USB spoofing
            if verify_identity:
                try:
                    manufacturer = self.device.manufacturer or ""
                    product = self.device.product or ""
                    if _EXPECTED_MANUFACTURER.lower() not in manufacturer.lower():
                        logger.warning(
                            "Unexpected manufacturer string '%s' (expected '%s') — "
                            "possible USB spoofing. Pass verify_identity=False to override.",
                            manufacturer, _EXPECTED_MANUFACTURER,
                        )
                        self.device = None
                        return False
                    if _EXPECTED_PRODUCT.lower() not in product.lower():
                        logger.warning(
                            "Unexpected product string '%s' (expected '%s') — "
                            "possible USB spoofing. Pass verify_identity=False to override.",
                            product, _EXPECTED_PRODUCT,
                        )
                        self.device = None
                        return False
                except _USBError as e:
                    # Some devices don't expose string descriptors; log and continue
                    logger.debug("Could not read device strings for identity check: %s", e)

            # Set configuration
            try:
                self.device.set_configuration()
            except _USBError as e:
                logger.debug("set_configuration failed (may already be set): %s", e)

            # Claim interface
            try:
                usb.util.claim_interface(self.device, 0)
            except _USBError:
                try:
                    usb.util.release_interface(self.device, 0)
                    usb.util.claim_interface(self.device, 0)
                except _USBError as e:
                    logger.warning("Failed to claim USB interface: %s", e)

            self.protocol = HantekProtocol(self.device)
            return True

        except _USBError as e:
            logger.error("USB error during connect: %s", e)
            return False

    def disconnect(self) -> None:
        """Disconnect from device."""
        if self.device is None:
            return
        # L1: guard against pyusb being torn down at interpreter shutdown
        if _HAVE_USB and usb is not None:
            try:
                usb.util.release_interface(self.device, 0)
            except Exception as e:
                logger.debug("release_interface during disconnect: %s", e)
        self.device = None
        self.protocol = None

    def initialize(self, timeout: int = 2000, inter_cmd_delay: float = 0.01) -> bool:
        """
        Initialize device (must be called after connect).

        Args:
            timeout: USB timeout in milliseconds
            inter_cmd_delay: Delay in seconds between init commands (L2)

        Returns:
            True if successful, False otherwise
        """
        if not self.protocol:
            return False

        return self.protocol.initialize(timeout, inter_cmd_delay=inter_cmd_delay)

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
        """
        if not self.protocol:
            return {}

        valid_channels = [ch for ch in channels if 1 <= ch <= 8]
        if not valid_channels:
            return {}

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
            command: Command bytes (must be bytes/bytearray, max HANTEK_PACKET_SIZE)
            timeout: USB timeout in milliseconds

        Returns:
            True if successful, False otherwise

        Raises:
            TypeError: if command is not bytes or bytearray
            ValueError: if command exceeds HANTEK_PACKET_SIZE
        """
        # H2: validate type and length before forwarding to USB layer
        if not isinstance(command, (bytes, bytearray)):
            raise TypeError(f"command must be bytes or bytearray, got {type(command).__name__}")
        if len(command) > HANTEK_PACKET_SIZE:
            raise ValueError(
                f"command length {len(command)} exceeds maximum packet size {HANTEK_PACKET_SIZE}"
            )

        if not self.protocol:
            return False

        return self.protocol.send_command(command, timeout)

    def read_response(self, size: int = 64, timeout: int = 1000) -> Optional[bytes]:
        """
        Read response from device.

        Args:
            size: Number of bytes to read (capped at 65536)
            timeout: USB timeout in milliseconds

        Returns:
            Response bytes, or None on error
        """
        # M2: cap unbounded size to prevent excessive memory allocation
        size = min(size, 65536)
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
        """Best-effort cleanup; prefer using as a context manager."""
        # L1: guard against partial interpreter shutdown
        try:
            self.disconnect()
        except Exception:
            pass
