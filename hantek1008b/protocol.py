"""
Hantek 1008B USB Protocol Implementation

Low-level protocol handling for USB communication with the device.
"""

from typing import Optional, List, Dict, Any
import struct
import time

try:
    import usb.core
    _HAVE_USB = True
except ImportError:
    _HAVE_USB = False

# USB Endpoints
HANTEK_ENDPOINT_OUT = 0x02  # Bulk OUT (Host to Device)
HANTEK_ENDPOINT_IN = 0x81   # Bulk IN (Device to Host)
HANTEK_PACKET_SIZE = 64     # Maximum packet size

# Device IDs
HANTEK_VID = 0x0783  # Hantek USB Vendor ID
HANTEK_PID = 0x5725  # Hantek 1008B Product ID


class HantekCommands:
    """USB command opcodes extracted from protocol capture."""
    
    # Status/Control Commands
    CMD_STATUS = b"\xf3"              # Status check
    CMD_SYNC = b"\xa5\x5a"           # Synchronization/handshake
    CMD_RESET = b"\xc0"              # Reset command
    
    # Initialization Commands
    CMD_INIT_1 = b"\xe4\x01"         # Initialization step 1
    CMD_INIT_2 = b"\xe6\x01"         # Initialization step 2
    CMD_INIT_3 = b"\xa4\x01"         # Initialization step 3
    
    # Channel Configuration
    CMD_CH_SET_1 = b"\xc6\x02"       # Channel setup variant 1
    CMD_CH_SET_2 = b"\xc6\x03"       # Channel setup variant 2
    
    # Data Acquisition Commands
    CMD_READ_1 = b"\xa6\x02"         # Read data command 1
    CMD_READ_2 = b"\xa6\x03"         # Read data command 2
    
    @staticmethod
    def get_init_sequence() -> List[bytes]:
        """Get device initialization command sequence."""
        return [
            HantekCommands.CMD_STATUS,      # F3 - Status check
            HantekCommands.CMD_INIT_1,       # E4 01 - Init step 1
            HantekCommands.CMD_INIT_2,       # E6 01 - Init step 2
            HantekCommands.CMD_INIT_3,       # A4 01 - Init step 3
            HantekCommands.CMD_RESET,        # C0 - Reset
            HantekCommands.CMD_SYNC,         # A5 5A - Sync/handshake
            HantekCommands.CMD_STATUS,      # F3 - Status check
            HantekCommands.CMD_SYNC,         # A5 5A - Sync/handshake
            HantekCommands.CMD_STATUS,       # F3 - Status check
            HantekCommands.CMD_SYNC,         # A5 5A - Sync/handshake
            HantekCommands.CMD_CH_SET_1,     # C6 02 - Channel setup
        ]


class HantekProtocol:
    """Low-level protocol handler for Hantek 1008B."""
    
    def __init__(self, device: Any):
        """
        Initialize protocol handler.
        
        Args:
            device: USB device object (from pyusb)
        """
        self.device = device
    
    def send_command(self, command: bytes, timeout: int = 1000) -> bool:
        """Send a command to the device."""
        if not _HAVE_USB or self.device is None:
            return False
        
        try:
            # Pad command to packet size
            padded = command + b"\x00" * (HANTEK_PACKET_SIZE - len(command))
            padded = padded[:HANTEK_PACKET_SIZE]
            
            # Send via bulk OUT endpoint
            bytes_written = self.device.write(HANTEK_ENDPOINT_OUT, padded, timeout)
            return bytes_written > 0
        except Exception:
            return False
    
    def read_response(self, size: int = HANTEK_PACKET_SIZE, timeout: int = 1000) -> Optional[bytes]:
        """Read response from device."""
        if not _HAVE_USB or self.device is None:
            return None
        
        try:
            data = self.device.read(HANTEK_ENDPOINT_IN, size, timeout)
            return bytes(data) if data else None
        except Exception:
            return None
    
    def initialize(self, timeout: int = 2000) -> bool:
        """Initialize device."""
        if self.device is None:
            return False
        
        try:
            init_commands = HantekCommands.get_init_sequence()
            
            for cmd in init_commands:
                if not self.send_command(cmd, timeout):
                    return False
                
                time.sleep(0.01)  # Small delay between commands
                self.read_response(HANTEK_PACKET_SIZE, timeout)  # Read ack if any
            
            return True
        except Exception:
            return False
    
    def read_data_packet(self, timeout: int = 1000) -> Optional[bytes]:
        """Read a single data packet."""
        if self.device is None:
            return None
        
        try:
            if not self.send_command(HantekCommands.CMD_READ_1, timeout):
                return None
            return self.read_response(HANTEK_PACKET_SIZE, timeout)
        except Exception:
            return None
    
    def read_multiple_packets(self, num_packets: int = 1, timeout: int = 1000) -> List[bytes]:
        """Read multiple data packets."""
        packets = []
        for _ in range(num_packets):
            packet = self.read_data_packet(timeout)
            if packet:
                packets.append(packet)
            else:
                break
        return packets
    
    def read_channels(
        self,
        channels: List[int],
        sample_count: int = 4096,
        voltage_range: float = 5.0,
        timeout: int = 3000,
    ) -> Dict[int, List[float]]:
        """Read data from specified channels."""
        if self.device is None:
            return {}
        
        # Calculate packets needed
        samples_per_packet = HANTEK_PACKET_SIZE // 2  # 32 samples per packet
        num_packets = (sample_count * len(channels) + samples_per_packet - 1) // samples_per_packet
        
        all_channel_data: Dict[int, List[int]] = {ch: [] for ch in channels}
        
        try:
            # Read packets
            packets = self.read_multiple_packets(num_packets, timeout)
            
            for packet_data in packets:
                if packet_data is None:
                    continue
                
                # Parse samples
                parsed_channels = self._parse_sample_data(packet_data, num_channels=8)
                if parsed_channels is None:
                    continue
                
                # Accumulate samples
                for idx, ch in enumerate(channels):
                    if idx < len(parsed_channels):
                        all_channel_data[ch].extend(parsed_channels[idx])
            
            # Convert to voltage and limit to requested count
        except Exception:
            return {}
        
        # Convert samples to voltage
        result: Dict[int, List[float]] = {}
        for ch in channels:
            samples = all_channel_data[ch][:sample_count]
            voltages = self._convert_samples_to_voltage(samples, voltage_range)
            result[ch] = voltages
        
        return result
    
    def _parse_sample_data(self, data: bytes, num_channels: int = 8) -> Optional[List[List[int]]]:
        """Parse sample data from USB packets."""
        if not data or len(data) < 2:
            return None
        
        try:
            # Parse as 16-bit little-endian, mask to 12 bits
            num_samples = len(data) // 2
            raw_samples = struct.unpack(f"<{num_samples}H", data[:num_samples * 2])
            samples_12bit = [s & 0xFFF for s in raw_samples]
            
            # Distribute across channels (interleaved hypothesis)
            samples_per_channel = []
            for ch in range(num_channels):
                channel_samples = [
                    samples_12bit[i] 
                    for i in range(ch, len(samples_12bit), num_channels)
                ]
                samples_per_channel.append(channel_samples)
            
            return samples_per_channel
        except Exception:
            # Fallback: sequential arrangement
            try:
                samples_per_packet = len(data) // 2
                samples_per_channel_count = samples_per_packet // num_channels
                
                raw_samples = struct.unpack(f"<{samples_per_packet}H", data[:samples_per_packet * 2])
                samples_12bit = [s & 0xFFF for s in raw_samples]
                
                samples_per_channel = []
                for ch in range(num_channels):
                    start_idx = ch * samples_per_channel_count
                    end_idx = start_idx + samples_per_channel_count
                    samples_per_channel.append(samples_12bit[start_idx:end_idx])
                
                return samples_per_channel
            except Exception:
                return None
    
    def _convert_samples_to_voltage(
        self,
        samples: List[int],
        voltage_range: float = 5.0,
        bits_per_sample: int = 12,
        offset: float = 0.0,
    ) -> List[float]:
        """Convert 12-bit ADC samples to voltage values."""
        max_value = (1 << bits_per_sample) - 1  # 4095 for 12-bit
        scale = voltage_range / max_value
        return [(sample * scale) + offset for sample in samples]

