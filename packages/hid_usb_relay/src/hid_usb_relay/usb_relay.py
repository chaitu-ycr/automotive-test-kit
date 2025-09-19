"""
This module provides functions to interact with a USB relay device using command-line commands.
It allows users to get and set the state of the relay device, as well as retrieve information about the relay device's status.
"""

import os
import platform
import subprocess
from typing import Optional, Tuple, List

def get_platform_and_architecture() -> Tuple[str, str]:
    """
    Get the current system platform and architecture.

    Returns:
        tuple: (system, architecture), both lowercase strings.
    """
    return platform.system().lower(), platform.architecture()[0].lower()

def get_bin_path() -> str:
    """
    Get the absolute path to the package's binary folder.

    Returns:
        str: Path to the binary folder.
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hid_usb_relay_bin')

def get_relay_path(file_name: str) -> str:
    """
    Build the path to a relay binary/library for the current platform and architecture.

    Args:
        file_name (str): Name of the binary/library file.

    Returns:
        str: Full path to the file.

    Raises:
        OSError: If the system platform is unsupported.
    """
    bin_dir = get_bin_path()
    system, arch = get_platform_and_architecture()
    if system not in ['windows', 'linux']:
        raise OSError(f'Unsupported system platform: {system}')
    return os.path.join(bin_dir, system, arch, file_name)

def get_relay_executable() -> str:
    """
    Get the path to the relay command-line executable for the current platform.

    Returns:
        str: Full path to the relay executable.
    """
    exe_name = "hidusb-relay-cmd.exe" if platform.system().lower() == 'windows' else "hidusb-relay-cmd"
    return get_relay_path(exe_name)

def get_relay_library() -> str:
    """
    Get the path to the relay library for the current platform.

    Returns:
        str: Full path to the relay library.
    """
    lib_name = "USB_RELAY_DEVICE.dll" if platform.system().lower() == 'windows' else "usb_relay_device.so"
    return get_relay_path(lib_name)

def run_command(command: List[str]) -> Optional[str]:
    """
    Run a command using subprocess and return its output.

    Args:
        command (List[str]): Command and arguments as a list.

    Returns:
        Optional[str]: Output string if successful, None otherwise.
    """
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if process.returncode == 0:
        return process.stdout.strip()
    print(f"Error executing command: {process.stderr}")
    return None

def get_default_relay_device_state() -> Optional[List[str]]:
    """
    Get the status of the default relay device.

    Returns:
        Optional[List[str]]: List of relay states, or None on error.
    """
    output = run_command([get_relay_executable(), "STATUS"])
    return output.split(':')[-1].strip().split(' ') if output else None

def set_default_relay_device_state(relay_state: str) -> bool:
    """
    Set all relays on the default device to a given state.

    Args:
        relay_state (str): "ON" or "OFF".

    Returns:
        bool: True if successful, False otherwise.
    """
    return run_command([get_relay_executable(), relay_state, "ALL"]) is not None

def get_relay_device_state(relay_id: str) -> Optional[List[str]]:
    """
    Get the status of a specific relay device by ID.

    Args:
        relay_id (str): Relay device ID.

    Returns:
        Optional[List[str]]: List of relay states, or None on error.
    """
    output = run_command([get_relay_executable(), f"id={relay_id}", "STATUS"])
    return output.split(':')[-1].strip().split(' ') if output else None

def set_relay_device_state(relay_id: str, relay_state: str) -> bool:
    """
    Set all relays on a specific device to a given state.

    Args:
        relay_id (str): Relay device ID.
        relay_state (str): "ON" or "OFF".

    Returns:
        bool: True if successful, False otherwise.
    """
    return run_command([get_relay_executable(), f"id={relay_id}", relay_state, "ALL"]) is not None

def get_all_relay_device_state() -> Optional[str]:
    """
    Get the status of all connected relay devices.

    Returns:
        Optional[str]: Status string, or None on error.
    """
    return run_command([get_relay_executable(), "ENUM"])

def get_relay_device_relay_state(relay_id: str, relay_number: str) -> Optional[str]:
    """
    Get the state of a specific relay on a specific device.

    Args:
        relay_id (str): Relay device ID.
        relay_number (str): Relay number as string (e.g., "1").

    Returns:
        Optional[str]: State ("ON"/"OFF") or None on error.
    """
    states = get_relay_device_state(relay_id)
    if states:
        return states[int(relay_number) - 1].split('=')[-1]
    return None

def set_relay_device_relay_state(relay_id: str, relay_number: str, relay_state: str) -> bool:
    """
    Set the state of a specific relay on a specific device.

    Args:
        relay_id (str): Relay device ID.
        relay_number (str): Relay number as string (e.g., "1").
        relay_state (str): "ON" or "OFF".

    Returns:
        bool: True if successful, False otherwise.
    """
    return run_command([get_relay_executable(), f"id={relay_id}", relay_state, relay_number]) is not None

def get_default_relay_device_relay_state(relay_number: str) -> Optional[str]:
    """
    Get the state of a specific relay on the default device.

    Args:
        relay_number (str): Relay number as string (e.g., "1").

    Returns:
        Optional[str]: State ("ON"/"OFF") or None on error.
    """
    states = get_default_relay_device_state()
    if states:
        return states[int(relay_number) - 1].split('=')[-1]
    return None

def set_default_relay_device_relay_state(relay_number: str, relay_state: str) -> bool:
    """
    Set the state of a specific relay on the default device.

    Args:
        relay_number (str): Relay number as string (e.g., "1").
        relay_state (str): "ON" or "OFF".

    Returns:
        bool: True if successful, False otherwise.
    """
    return run_command([get_relay_executable(), relay_state, relay_number]) is not None
