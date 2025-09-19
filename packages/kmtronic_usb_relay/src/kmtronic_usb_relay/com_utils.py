import logging
from typing import Any, Dict, List, Optional, Union

import serial
import serial.tools.list_ports

logger = logging.getLogger(__name__)

class SerialComUtils:
    """
    User-friendly utility class for serial COM port communication.

    This class provides methods for discovering available serial ports,
    connecting/disconnecting to a port, and sending/receiving data.
    It also supports context management for safe resource handling.
    """

    # --- Initialization and Configuration ---

    def __init__(
        self,
        baudrate: int = 9600,
        bytesize: int = serial.EIGHTBITS,
        stopbits: int = serial.STOPBITS_ONE,
        parity: str = serial.PARITY_NONE,
        timeout: Optional[float] = 2.5,
    ):
        """
        Initialize SerialComUtils with serial parameters.

        Args:
            baudrate (int): Serial baudrate (default: 9600).
            bytesize (int): Number of data bits (default: serial.EIGHTBITS).
            stopbits (int): Number of stop bits (default: serial.STOPBITS_ONE).
            parity (str): Parity setting (default: serial.PARITY_NONE).
            timeout (float, optional): Read timeout in seconds, or None for blocking mode (default: 2.5).
        """
        self.connection: Optional[serial.Serial] = None
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.parity = parity
        self.timeout = timeout

    def get_connection_params(self) -> Dict[str, Any]:
        """
        Get the current serial connection parameters.

        Returns:
            dict: Dictionary containing baudrate, bytesize, stopbits, parity, and timeout.
        """
        return {
            "baudrate": self.baudrate,
            "bytesize": self.bytesize,
            "stopbits": self.stopbits,
            "parity": self.parity,
            "timeout": self.timeout,
        }

    def __repr__(self) -> str:
        """
        Return a string representation of the SerialComUtils instance.

        Returns:
            str: Human-readable summary of the current configuration and port.
        """
        port = self.connection.port if self.connection and self.connection.is_open else None
        return (
            f"<SerialComUtils(port={port}, baudrate={self.baudrate}, "
            f"bytesize={self.bytesize}, stopbits={self.stopbits}, "
            f"parity={self.parity}, timeout={self.timeout})>"
        )

    # --- Port Discovery and Info ---

    @staticmethod
    def get_port_names() -> List[str]:
        """
        List all available COM port device names.

        Returns:
            List[str]: List of device names (e.g., ['COM1', 'COM2']).
        """
        return [port.device for port in serial.tools.list_ports.comports()]

    @staticmethod
    def get_port_details() -> List[Dict[str, Any]]:
        """
        Get details of all available COM ports.

        Returns:
            List[dict]: Each dict contains:
                - device (str): COM port number (e.g., 'COM1')
                - description (str): Port description
                - hwid (str): Hardware ID
        """
        return [
            {
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid
            }
            for port in serial.tools.list_ports.comports()
        ]

    @staticmethod
    def format_port_detail(port_info: Dict[str, Any]) -> str:
        """
        Format a port info dictionary as a readable string.

        Args:
            port_info (dict): Dictionary with keys 'device', 'description', 'hwid'.

        Returns:
            str: Formatted string describing the port.
        """
        return (
            f"Device: {port_info['device']}, "
            f"Description: {port_info['description']}, "
            f"HWID: {port_info['hwid']}"
        )

    @staticmethod
    def log_port_details(port_name: Optional[str] = None) -> None:
        """
        Log details of all COM ports or a specific port if port_name is given.

        Args:
            port_name (str, optional): Device name of the port (e.g., 'COM3').
        """
        ports = SerialComUtils.get_port_details()
        if port_name:
            for port in ports:
                if port["device"] == port_name:
                    logger.info(SerialComUtils.format_port_detail(port))
                    return
            logger.warning(f"Port {port_name} not found.")
        else:
            for port in ports:
                logger.info(SerialComUtils.format_port_detail(port))

    @staticmethod
    def get_busy_ports() -> List[str]:
        """
        Attempt to list COM ports that are currently in use (best effort).

        Returns:
            List[str]: List of port device names that are in use.
        """
        busy_ports = []
        for port in SerialComUtils.get_port_names():
            try:
                with serial.Serial(port) as s:
                    pass
            except (OSError, serial.SerialException):
                busy_ports.append(port)
        return busy_ports

    # --- Connection Management ---

    @property
    def is_connected(self) -> bool:
        """
        Check if the serial connection is open.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self.connection is not None and self.connection.is_open

    def connect(self, port: str) -> bool:
        """
        Open a connection to a COM port with the configured parameters.

        Args:
            port (str): Device name of the port (e.g., 'COM3').

        Returns:
            bool: True if connection was successful, False otherwise.
        """
        try:
            self.connection = serial.Serial(
                port=port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                stopbits=self.stopbits,
                parity=self.parity,
                timeout=self.timeout
            )
            logger.info(f"Connected to {port}")
            return True
        except serial.SerialException as e:
            logger.error(f"Failed to connect to {port}: {e}")
            self.connection = None
            return False

    def open_connection(self, port: str) -> bool:
        """
        Alias for connect. Opens a connection to the specified port.

        Args:
            port (str): Device name of the port.

        Returns:
            bool: True if connection was successful, False otherwise.
        """
        return self.connect(port)

    def disconnect(self) -> bool:
        """
        Alias for close_connection. Closes the serial connection.

        Returns:
            bool: True if disconnected or already closed, False if error occurred.
        """
        return self.close_connection()

    def close_connection(self) -> bool:
        """
        Close the connection to the COM port.

        Returns:
            bool: True if disconnected or already closed, False if error occurred.
        """
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
                logger.info("Disconnected.")
                self.connection = None
                return True
            except Exception as e:
                logger.error(f"Error while disconnecting: {e}")
                return False
        self.connection = None
        return True

    # --- Data Transfer ---

    def send(self, data: bytes) -> bool:
        """
        Send data to the serial port.

        Args:
            data (bytes): Bytes to send.

        Returns:
            bool: True if sent, False if not connected.
        """
        if self.is_connected:
            self.connection.write(data)
            return True
        else:
            logger.warning("No open connection. Cannot send data.")
            return False

    def receive(self, size: int = 1, as_int_list: bool = False) -> Optional[Union[bytes, List[int]]]:
        """
        Receive data from the serial port.

        Args:
            size (int): Number of bytes to read (default: 1).
            as_int_list (bool): If True, return a list of ints instead of bytes.

        Returns:
            bytes or List[int] or None: Received data, or None if not connected.
        """
        if self.is_connected:
            data = self.connection.read(size)
            if as_int_list:
                return list(data)
            return data
        else:
            logger.warning("No open connection. Cannot receive data.")
            return None

    # --- Context Management ---

    def __enter__(self) -> "SerialComUtils":
        """
        Enter the runtime context related to this object.

        Returns:
            SerialComUtils: The instance itself.
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """
        Exit the runtime context and close the serial connection.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        self.close_connection()


