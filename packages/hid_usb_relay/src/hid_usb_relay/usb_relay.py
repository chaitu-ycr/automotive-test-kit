"""
HID USB Relay Controller Module

Provides an object-oriented interface for controlling HID USB relay devices
via command-line executable. Supports multiple relay devices with proper
error handling, validation, and reusability.

Example:
    >>> relay = USBRelayDevice()  # Default device
    >>> relay.turn_on(1)
    >>> relay.get_state()
    {'R1': 'ON', 'R2': 'OFF'}

    >>> specific = USBRelayDevice(device_id='HURTM')
    >>> specific.turn_on_all()

    >>> # Context manager pattern
    >>> with USBRelayDevice('HURTM') as relay:
    ...     relay.turn_on_all()
"""

import logging
import os
import platform
import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Union

__all__ = [
    'USBRelayDevice',
    'enumerate_devices',
    'RelayState',
    'RelayError',
    'RelayCommandError',
    'RelayValidationError',
]

# Configure module logger
logger = logging.getLogger(__name__)

# Constants
DEFAULT_TIMEOUT = 5.0
MAX_RELAY_COUNT = 8


class RelayState(Enum):
    """Relay state enumeration."""
    ON = "on"
    OFF = "off"


class RelayCommand(Enum):
    """Available relay commands."""
    STATE = "state"
    ENUM = "enum"


class RelayError(Exception):
    """Base exception for relay operations."""
    pass


class RelayCommandError(RelayError):
    """Raised when relay command execution fails."""
    pass


class RelayValidationError(RelayError):
    """Raised when input validation fails."""
    pass


@dataclass(frozen=True)
class PlatformInfo:
    """Platform and architecture information."""
    system: str
    architecture: str

    @property
    def is_windows(self) -> bool:
        return self.system == 'windows'

    @property
    def is_linux(self) -> bool:
        return self.system == 'linux'

    @property
    def arch_bits(self) -> str:
        """Get architecture as bit string (32bit/64bit)."""
        return '64bit' if '64' in self.architecture else '32bit'


@lru_cache(maxsize=1)
def get_platform_info() -> PlatformInfo:
    """
    Get cached platform information.

    Returns:
        PlatformInfo: Platform and architecture details.
    """
    return PlatformInfo(
        system=platform.system().lower(),
        architecture=platform.architecture()[0].lower()
    )


def _get_module_bin_directory() -> Path:
    """Get the default binaries folder in module directory."""
    return Path(__file__).parent / 'hid_usb_relay_bin'


def get_bin_directory(base_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Get the absolute path to the binaries folder.

    Args:
        base_path: Optional custom base path. If None, uses module directory.

    Returns:
        Path: Path to the binary folder.
    """
    if base_path is None:
        return _get_module_bin_directory()
    return Path(base_path) / 'hid_usb_relay_bin'


@lru_cache(maxsize=1)
def _get_default_executable_path() -> Path:
    """Get cached default executable path."""
    plat = get_platform_info()

    if not (plat.is_windows or plat.is_linux):
        raise RelayError(f'Unsupported platform: {plat.system}')

    bin_dir = _get_module_bin_directory()
    exe_name = "hidusb-relay-cmd.exe" if plat.is_windows else "hidusb-relay-cmd"
    exe_path = bin_dir / plat.system / plat.arch_bits / exe_name

    if not exe_path.exists():
        raise RelayError(f'Executable not found: {exe_path}')

    return exe_path


def get_executable_path(base_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Get the path to the relay command-line executable.

    Args:
        base_path: Optional custom base path for binaries. If None, uses cached default.

    Returns:
        Path: Full path to the relay executable.

    Raises:
        RelayError: If platform is unsupported or executable not found.
    """
    if base_path is None:
        return _get_default_executable_path()

    plat = get_platform_info()

    if not (plat.is_windows or plat.is_linux):
        raise RelayError(f'Unsupported platform: {plat.system}')

    bin_dir = get_bin_directory(base_path)
    exe_name = "hidusb-relay-cmd.exe" if plat.is_windows else "hidusb-relay-cmd"
    exe_path = bin_dir / plat.system / plat.arch_bits / exe_name

    if not exe_path.exists():
        raise RelayError(f'Executable not found: {exe_path}')

    return exe_path


def _execute_command(command: List[str], timeout: float = DEFAULT_TIMEOUT) -> str:
    """
    Execute a relay command and return output.

    Args:
        command: Command and arguments as list.
        timeout: Command timeout in seconds.

    Returns:
        str: Command output (empty string if no output).

    Raises:
        RelayCommandError: If command execution fails.
    """
    # Convert Path objects to strings for subprocess
    cmd_str = [str(c) for c in command]
    logger.debug(f"Executing: {' '.join(cmd_str)}")

    try:
        result = subprocess.run(
            cmd_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            timeout=timeout
        )
        output = result.stdout.strip() if result.stdout else ""
        if output:
            logger.debug(f"Output: {output}")
        return output

    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed (exit {e.returncode}): {e.stderr.strip() if e.stderr else 'Unknown error'}"
        logger.error(error_msg)
        raise RelayCommandError(error_msg) from e
    except subprocess.TimeoutExpired as e:
        error_msg = f"Command timed out after {timeout}s"
        logger.error(error_msg)
        raise RelayCommandError(error_msg) from e
    except FileNotFoundError as e:
        error_msg = f"Executable not found: {command[0]}"
        logger.error(error_msg)
        raise RelayCommandError(error_msg) from e
    except OSError as e:
        error_msg = f"OS error executing command: {e}"
        logger.error(error_msg)
        raise RelayCommandError(error_msg) from e


def _parse_relay_states(output: str) -> Dict[str, str]:
    """
    Parse relay state output into a dictionary.

    Args:
        output: Raw command output (e.g., "Board ID=[BITFT] State: R1=OFF R2=OFF").

    Returns:
        Dict mapping relay names to states (e.g., {'R1': 'OFF', 'R2': 'OFF'}).

    Raises:
        RelayError: If output format is invalid.
    """
    if not output or 'State:' not in output:
        raise RelayError(f"Invalid state format: {output}")

    # Extract state portion after "State:"
    state_str = output.split('State:', 1)[-1].strip()

    # Parse relay states using regex for robustness
    # Matches patterns like R1=OFF, R2=ON
    pattern = re.compile(r'(R\d+)=(ON|OFF)', re.IGNORECASE)
    matches = pattern.findall(state_str)

    if not matches:
        raise RelayError(f"No relay states found in: {output}")

    return {relay: state.upper() for relay, state in matches}


def _validate_relay_number(relay_num: Union[int, str], max_relays: int = MAX_RELAY_COUNT) -> int:
    """
    Validate and convert relay number.

    Args:
        relay_num: Relay number as int or string.
        max_relays: Maximum valid relay number.

    Returns:
        int: Validated relay number.

    Raises:
        RelayValidationError: If relay number is invalid.
    """
    try:
        num = int(relay_num)
    except (ValueError, TypeError) as e:
        raise RelayValidationError(
            f"Invalid relay number format: {relay_num!r}"
        ) from e

    if not 1 <= num <= max_relays:
        raise RelayValidationError(
            f"Relay number must be between 1 and {max_relays}, got {num}"
        )

    return num


class USBRelayDevice:
    """
    Interface for controlling a USB relay device.

    Supports context manager protocol for resource management patterns.

    Attributes:
        device_id: Optional device ID. If None, uses default device.

    Example:
        >>> relay = USBRelayDevice(device_id='HURTM')
        >>> relay.turn_on(1)
        >>> relay.get_state()
        {'R1': 'ON', 'R2': 'OFF'}

        >>> with USBRelayDevice('HURTM') as relay:
        ...     relay.turn_on_all()
    """

    def __init__(
        self,
        device_id: Optional[str] = None,
        executable_path: Optional[Union[str, Path]] = None,
        timeout: float = DEFAULT_TIMEOUT
    ):
        """
        Initialize relay device controller.

        Args:
            device_id: Device ID. If None, controls the default device.
            executable_path: Custom path to relay executable. If None, auto-detects.
            timeout: Command timeout in seconds.
        """
        self.device_id = device_id
        self._timeout = timeout
        self._exe_path = Path(executable_path) if executable_path else get_executable_path()
        logger.info(f"Initialized USB relay: {device_id or 'default'}")

    def __enter__(self) -> 'USBRelayDevice':
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        # Could add cleanup logic here if needed
        pass

    def __repr__(self) -> str:
        return f"USBRelayDevice(device_id={self.device_id!r})"

    def _build_command(
        self,
        action: str,
        target: Optional[str] = None
    ) -> List[Union[Path, str]]:
        """
        Build command list for execution.

        Args:
            action: Action to perform (on/off/state/enum).
            target: Target relay number or "all".

        Returns:
            List of command arguments.
        """
        cmd: List[Union[Path, str]] = [self._exe_path]

        if self.device_id:
            cmd.append(f"id={self.device_id}")

        cmd.append(action)

        if target is not None:
            cmd.append(target)

        return cmd

    def _execute(self, action: str, target: Optional[str] = None) -> str:
        """Execute command with device-specific timeout."""
        cmd = self._build_command(action, target)
        return _execute_command(cmd, timeout=self._timeout)

    def get_state(self) -> Dict[str, str]:
        """
        Get current state of all relays on this device.

        Returns:
            Dict mapping relay names to states (e.g., {'R1': 'ON', 'R2': 'OFF'}).

        Raises:
            RelayCommandError: If command fails.
        """
        output = self._execute(RelayCommand.STATE.value)
        return _parse_relay_states(output)

    def get_relay_state(self, relay_num: Union[int, str]) -> str:
        """
        Get state of a specific relay.

        Args:
            relay_num: Relay number (1-based).

        Returns:
            str: "ON" or "OFF".

        Raises:
            RelayValidationError: If relay number is invalid.
            RelayCommandError: If command fails.
            RelayError: If relay not found.
        """
        num = _validate_relay_number(relay_num)
        states = self.get_state()
        relay_key = f"R{num}"

        if relay_key not in states:
            raise RelayError(
                f"Relay {num} not found. Available: {', '.join(states.keys())}"
            )

        return states[relay_key]

    def set_state(
        self,
        state: Union[RelayState, str],
        relay_num: Optional[Union[int, str]] = None
    ) -> None:
        """
        Set relay state.

        Args:
            state: RelayState.ON/OFF or "on"/"off"/"ON"/"OFF" string.
            relay_num: Optional relay number. If None, sets all relays.

        Raises:
            RelayValidationError: If inputs are invalid.
            RelayCommandError: If command fails.
        """
        # Normalize state
        if isinstance(state, RelayState):
            state_str = state.value
        elif isinstance(state, str):
            state_str = state.lower()
            if state_str not in ('on', 'off'):
                raise RelayValidationError(
                    f"Invalid state: {state!r}. Must be 'on' or 'off'"
                )
        else:
            raise RelayValidationError(
                f"State must be RelayState or str, got {type(state).__name__}"
            )

        # Determine target
        if relay_num is None:
            target = "all"
        else:
            num = _validate_relay_number(relay_num)
            target = str(num)

        self._execute(state_str, target)
        logger.info(f"Set {self.device_id or 'default'} relay {target} to {state_str.upper()}")

    def turn_on(self, relay_num: Union[int, str]) -> None:
        """Turn on a specific relay."""
        self.set_state(RelayState.ON, relay_num)

    def turn_off(self, relay_num: Union[int, str]) -> None:
        """Turn off a specific relay."""
        self.set_state(RelayState.OFF, relay_num)

    def turn_on_all(self) -> None:
        """Turn on all relays."""
        self.set_state(RelayState.ON)

    def turn_off_all(self) -> None:
        """Turn off all relays."""
        self.set_state(RelayState.OFF)


def enumerate_devices() -> List[Dict[str, str]]:
    """
    Enumerate all connected relay devices.

    Returns:
        List of dicts containing device info and states.
        Example: [
            {'device_id': 'BITFT', 'R1': 'OFF', 'R2': 'OFF'},
            {'device_id': 'HURTM', 'R1': 'ON', 'R2': 'ON'}
        ]

    Raises:
        RelayCommandError: If enumeration fails.
    """
    exe_path = _get_default_executable_path()
    output = _execute_command([exe_path, RelayCommand.ENUM.value])

    # Regex to extract device ID more robustly
    device_pattern = re.compile(r'Board ID=\[([^\]]+)\]', re.IGNORECASE)

    devices = []
    for line in output.split('\n'):
        if not line.strip():
            continue

        match = device_pattern.search(line)
        if match:
            device_id = match.group(1)
            try:
                states = _parse_relay_states(line)
                devices.append({'device_id': device_id, **states})
            except RelayError as e:
                logger.warning(f"Failed to parse device {device_id}: {e}")

    logger.info(f"Found {len(devices)} relay device(s)")
    return devices


# Backward compatibility functions (delegating to class-based API)
def get_default_relay_device_state() -> Optional[List[str]]:
    """DEPRECATED: Use USBRelayDevice().get_state() instead."""
    try:
        states = USBRelayDevice().get_state()
        return [f"{k}={v}" for k, v in states.items()]
    except RelayError:
        return None


def set_default_relay_device_state(relay_state: str) -> bool:
    """DEPRECATED: Use USBRelayDevice().set_state() instead."""
    try:
        USBRelayDevice().set_state(relay_state)
        return True
    except RelayError:
        return False


def get_relay_device_state(relay_id: str) -> Optional[List[str]]:
    """DEPRECATED: Use USBRelayDevice(device_id).get_state() instead."""
    try:
        states = USBRelayDevice(device_id=relay_id).get_state()
        return [f"{k}={v}" for k, v in states.items()]
    except RelayError:
        return None


def set_relay_device_state(relay_id: str, relay_state: str) -> bool:
    """DEPRECATED: Use USBRelayDevice(device_id).set_state() instead."""
    try:
        USBRelayDevice(device_id=relay_id).set_state(relay_state)
        return True
    except RelayError:
        return False


def get_all_relay_device_state() -> Optional[str]:
    """DEPRECATED: Use enumerate_devices() instead."""
    try:
        exe_path = get_executable_path()
        return _execute_command([exe_path, RelayCommand.ENUM.value])
    except RelayError:
        return None


def get_relay_device_relay_state(relay_id: str, relay_number: str) -> Optional[str]:
    """DEPRECATED: Use USBRelayDevice(device_id).get_relay_state() instead."""
    try:
        return USBRelayDevice(device_id=relay_id).get_relay_state(relay_number)
    except RelayError:
        return None


def set_relay_device_relay_state(relay_id: str, relay_number: str, relay_state: str) -> bool:
    """DEPRECATED: Use USBRelayDevice(device_id).set_state() instead."""
    try:
        USBRelayDevice(device_id=relay_id).set_state(relay_state, relay_number)
        return True
    except RelayError:
        return False


def get_default_relay_device_relay_state(relay_number: str) -> Optional[str]:
    """DEPRECATED: Use USBRelayDevice().get_relay_state() instead."""
    try:
        return USBRelayDevice().get_relay_state(relay_number)
    except RelayError:
        return None


def set_default_relay_device_relay_state(relay_number: str, relay_state: str) -> bool:
    """DEPRECATED: Use USBRelayDevice().set_state() instead."""
    try:
        USBRelayDevice().set_state(relay_state, relay_number)
        return True
    except RelayError:
        return False
