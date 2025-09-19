import logging
from typing import Optional, Type

import serial
import serial.tools.list_ports
from tenma import instantiate_tenma_class_from_device_response

logging.basicConfig(level=logging.INFO)


class TenmaPs:
    """
    Interface for a Tenma power supply device.

    This class manages connection to a Tenma power supply, allowing users to
    retrieve device status and control voltage/current settings.

    Attributes:
        VOLTAGE_MULTIPLIER (float): Multiplier to convert volts to millivolts.
        CURRENT_MULTIPLIER (float): Multiplier to convert amps to milliamps.

    Example:
        ```python
        from tenma_ps.power_supply import TenmaPs

        with TenmaPs("COM4") as tenma_ps:
            print("Device version:", tenma_ps.get_version())
            print("Device status:", tenma_ps.get_status())

            # Set voltage and current on channel 1
            tenma_ps.set_voltage(channel=1, voltage=5.0)
            tenma_ps.set_current(channel=1, current=1.0)

            # Read voltage and current from channel 1
            voltage = tenma_ps.read_voltage(channel=1)
            current = tenma_ps.read_current(channel=1)
            print(f"Channel 1 Voltage: {voltage} V")
            print(f"Channel 1 Current: {current} A")

            # Turn on and off the power supply
            tenma_ps.turn_on()
            print("Power supply turned ON.")
            tenma_ps.turn_off()
            print("Power supply turned OFF.")
        ```
    """

    VOLTAGE_MULTIPLIER: float = 1000.0  # To convert volts to millivolts
    CURRENT_MULTIPLIER: float = 1000.0  # To convert amps to milliamps

    def __init__(self, port: str) -> None:
        """
        Initialize the Tenma power supply interface.

        Args:
            port (str): The COM port (e.g., "COM4") to which the device is connected.

        Raises:
            Exception: If the connection to the device fails.
        """
        self._close_com_port_if_open(port)
        self.device = instantiate_tenma_class_from_device_response(port)

    def _close_com_port_if_open(self, port: str) -> None:
        """
        Close the COM port if it is already open.

        Args:
            port (str): The COM port to check and close if open.

        Logs:
            Logs a message if the port is successfully closed.
            Logs an error if there is an issue closing the port.
        """
        try:
            for p in serial.tools.list_ports.comports():
                if p.device == port:
                    try:
                        with serial.Serial(port) as ser:
                            if ser.is_open:
                                ser.close()
                                logging.info(f"Closed COM port: {port}")
                    except serial.SerialException as e:
                        logging.error(f"Error closing COM port {port}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error closing COM port {port}: {e}")

    def get_version(self) -> str:
        """
        Get the version information of the Tenma power supply.

        Returns:
            str: The version string reported by the device.
        """
        return self.device.getVersion()

    def get_status(self) -> str:
        """
        Get the current status of the Tenma power supply.

        Returns:
            str: The status string reported by the device.
        """
        return self.device.getStatus()

    def turn_on(self) -> None:
        """
        Power on the Tenma power supply.
        """
        self.device.ON()

    def turn_off(self) -> None:
        """
        Power off the Tenma power supply.
        """
        self.device.OFF()

    def read_voltage(self, channel: int) -> float:
        """
        Read the voltage from a specified channel.

        Args:
            channel (int): The channel number to read from.

        Returns:
            float: The voltage value in volts.
        """
        return self.device.runningVoltage(channel)

    def read_current(self, channel: int) -> float:
        """
        Read the current from a specified channel.

        Args:
            channel (int): The channel number to read from.

        Returns:
            float: The current value in amps.
        """
        return self.device.runningCurrent(channel)

    def set_voltage(self, channel: int, voltage: float) -> None:
        """
        Set the voltage for a specified channel.

        Args:
            channel (int): The channel number to set.
            voltage (float): The voltage value in volts.
        """
        self.device.setVoltage(channel, voltage * self.VOLTAGE_MULTIPLIER)

    def set_current(self, channel: int, current: float) -> None:
        """
        Set the current for a specified channel.

        Args:
            channel (int): The channel number to set.
            current (float): The current value in amps.
        """
        self.device.setCurrent(channel, current * self.CURRENT_MULTIPLIER)

    def close(self) -> None:
        """
        Close the connection to the Tenma power supply.
        """
        self.device.close()

    def __enter__(self) -> "TenmaPs":
        """
        Enter the runtime context for the TenmaPs object.

        Returns:
            TenmaPs: The TenmaPs instance.
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[object]
    ) -> None:
        """
        Exit the runtime context and clean up resources.

        Args:
            exc_type (Optional[Type[BaseException]]): Exception type, if any.
            exc_value (Optional[BaseException]): Exception value, if any.
            traceback (Optional[object]): Traceback object, if any.
        """
        self.close()


if __name__ == "__main__":
    pass
