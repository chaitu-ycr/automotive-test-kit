from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from py_uds_demo.core.server import UdsServer


class InputOutputControlByIdentifier:
    """
    Handles Input Output Control By Identifier (0x2F) service requests.

    What:
        This service allows a client to take control of a server's (ECU's)
        inputs and outputs.

    Why:
        It's used for testing and diagnostics. For example, a technician can
        use it to manually activate an actuator (like a fan or a motor) to
        verify its operation, or to simulate a sensor input to see how the
        ECU responds.

    How:
        The client sends a request with the SID 0x2F, a Data Identifier (DID)
        to specify the I/O channel, and a control option (e.g., return
        control to ECU, freeze current state, short term adjustment).

    Real-world example:
        A technician suspects a radiator fan is faulty. They use a diagnostic
        tool to send an Input Output Control By Identifier request to the
        engine control unit, commanding it to turn on the fan. If the fan
        starts, the technician knows the fan motor is working and the issue
        lies elsewhere, perhaps with the temperature sensor or control logic.

    Attributes:
        uds_server: The UDS server instance.
        io_control_status: A dictionary to store the status of I/O controls.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.io_control_status = {}

    def process_request(self, data_stream: list) -> list:
        """
        Processes an Input Output Control By Identifier request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) < 4:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.IOCBI, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        did = (data_stream[1] << 8) | data_stream[2]
        control_option = data_stream[3]

        # In a real ECU, you would check if the DID is valid for I/O control
        # and if the control option is supported.

        self.io_control_status[did] = control_option

        return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.IOCBI, data_stream[1:3])
