import logging
import time
from typing import Dict, List, Optional

from kmtronic_usb_relay.com_utils import SerialComUtils

logger = logging.getLogger(__name__)

class RelayController:
    """Controller for KMTronic 4-Channel USB Relay devices.

    Example:
        with RelayController("COM4") as relay:
            relay.turn_on(1)
            relay.turn_off(2)
            print(relay.statuses)
    """

    RELAY_COUNT = 4
    STATUS_ON = "ON"
    STATUS_OFF = "OFF"

    def __init__(
        self,
        com_port: str,
        switch_delay: float = 1.0,
        serial_utils: Optional[SerialComUtils] = None,
        auto_connect: bool = True,
    ):
        """
        Initialize the RelayController.

        Args:
            com_port (str): The COM port to which the relay board is connected (e.g., 'COM4').
            switch_delay (float): Delay in seconds after switching a relay (default: 1.0).
            serial_utils (Optional[SerialComUtils]): Custom SerialComUtils instance for testing/mocking.
            auto_connect (bool): Automatically open connection on init (default: True).
        """
        self.com_port = com_port
        self.switch_delay = switch_delay
        self.serial_utils = serial_utils or SerialComUtils()
        self._is_connected = False
        if auto_connect:
            self.connect()

    @property
    def is_connected(self) -> bool:
        """
        Check if the relay controller is connected to the COM port.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self.serial_utils.is_connected if self.serial_utils else False

    def connect(self) -> None:
        """
        Open the serial connection to the relay board.

        Raises:
            Exception: If the connection cannot be established.
        """
        if not self.is_connected:
            try:
                self._is_connected = self.serial_utils.open_connection(self.com_port)
                logger.info(f"Connected to relay on {self.com_port}")
            except Exception as e:
                logger.error(f"Failed to open serial connection on {self.com_port}: {e}")
                raise

    def close(self) -> None:
        """
        Close the serial connection to the relay board.

        This method is safe to call multiple times.
        """
        try:
            result = self.serial_utils.close_connection()
            self._is_connected = not result
            logger.info("Serial connection closed.")
        except Exception as e:
            logger.warning(f"Error closing serial connection: {e}")

    def turn_on(self, relay_number: int) -> None:
        """
        Turn ON the specified relay.

        Args:
            relay_number (int): Relay number to turn ON (1-4).

        Raises:
            ValueError: If relay_number is out of range.
            Exception: If sending the command fails.
        """
        self._validate_relay_number(relay_number)
        self._send_relay_command(relay_number, True)

    def turn_off(self, relay_number: int) -> None:
        """
        Turn OFF the specified relay.

        Args:
            relay_number (int): Relay number to turn OFF (1-4).

        Raises:
            ValueError: If relay_number is out of range.
            Exception: If sending the command fails.
        """
        self._validate_relay_number(relay_number)
        self._send_relay_command(relay_number, False)

    @property
    def statuses(self) -> Dict[str, str]:
        """
        Get the status of all relays as a dictionary.

        Returns:
            Dict[str, str]: Dictionary mapping relay names (e.g., 'R1') to their status ('ON' or 'OFF').
        """
        return self.get_statuses()

    def get_statuses(self) -> Dict[str, str]:
        """
        Query and return the status of all relays.

        Returns:
            Dict[str, str]: Dictionary mapping relay names (e.g., 'R1') to their status ('ON' or 'OFF').
            Returns an empty dict if communication fails.
        """
        status_cmd = bytes([0xFF, 0x09, 0x00])
        try:
            self.serial_utils.send(status_cmd)
            response: Optional[List[int]] = self.serial_utils.receive(
                self.RELAY_COUNT, as_int_list=True
            )
        except Exception as e:
            logger.error(f"Failed to communicate with relay board: {e}")
            return {}

        if not response or len(response) < self.RELAY_COUNT:
            logger.error("Failed to read relay status or incomplete response.")
            return {}

        relay_status = {
            f"R{i}": self.STATUS_ON if byte == 1 else self.STATUS_OFF
            for i, byte in enumerate(response, start=1)
        }
        logger.info("Relay statuses: %s", ", ".join(f"{k}: {v}" for k, v in relay_status.items()))
        return relay_status

    def __enter__(self) -> "RelayController":
        """
        Enter the runtime context related to this object.

        Returns:
            RelayController: The connected relay controller instance.
        """
        self.connect()
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
        self.close()

    # --- Internal helpers ---

    def _send_relay_command(self, relay_number: int, turn_on: bool) -> None:
        """
        Send a command to turn a relay ON or OFF.

        Args:
            relay_number (int): Relay number (1-4).
            turn_on (bool): True to turn ON, False to turn OFF.

        Raises:
            Exception: If sending the command fails.
        """
        cmd = bytes([0xFF, relay_number, 0x01 if turn_on else 0x00])
        logger.debug(
            "Sending command: %s to relay %d (%s)",
            cmd.hex(), relay_number, "ON" if turn_on else "OFF"
        )
        try:
            self.serial_utils.send(cmd)
            time.sleep(self.switch_delay)
        except Exception as e:
            logger.error(f"Failed to send command to relay {relay_number}: {e}")
            raise

    def _validate_relay_number(self, relay_number: int) -> None:
        """
        Validate that the relay number is within the allowed range.

        Args:
            relay_number (int): Relay number to validate.

        Raises:
            ValueError: If relay_number is not between 1 and RELAY_COUNT.
        """
        if not (1 <= relay_number <= self.RELAY_COUNT):
            raise ValueError(
                f"relay_number must be between 1 and {self.RELAY_COUNT}, got {relay_number}."
            )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Hello Kmtronic USB Relay User!")

    # Example: Using RelayController directly
    print("\n--- Example: RelayController ---")
    try:
        with RelayController("COM4") as relay:
            relay.turn_on(1)
            relay.turn_off(2)
            print(f"Relay statuses: {relay.statuses}")
    except Exception as e:
        print(f"Error: {e}")
