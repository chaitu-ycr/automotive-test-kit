from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from py_uds_demo.core.server import UdsServer


class RoutineControl:
    """
    Handles Routine Control (0x31) service requests.

    What:
        This service is used to start, stop, and request the results of a
        routine in the server (ECU).

    Why:
        Routines are used to perform more complex tasks than what can be
        achieved with a simple read or write service. This can include
        things like running a self-test, erasing memory, or learning new
        adaptive values.

    How:
        The client sends a request with the SID 0x31, a sub-function
        (e.g., startRoutine, stopRoutine, requestRoutineResults), and a
        2-byte routine identifier.

    Real-world example:
        A technician wants to perform a self-test on the ABS. They use a
        diagnostic tool to send a Routine Control request with the
        'startRoutine' sub-function and the routine identifier for the ABS
        self-test. After the routine completes, they send another request
        with 'requestRoutineResults' to check if the test passed.

    Attributes:
        uds_server: The UDS server instance.
        routine_status: A dictionary to store the status of routines.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.routine_status = {}

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Routine Control request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) < 4:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.RC, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        sub_function = data_stream[1]
        routine_id = (data_stream[2] << 8) | data_stream[3]

        if sub_function == self.uds_server.SFID.START_ROUTINE:
            self.routine_status[routine_id] = "Started"
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.RC, data_stream[1:4])

        elif sub_function == self.uds_server.SFID.STOP_ROUTINE:
            self.routine_status[routine_id] = "Stopped"
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.RC, data_stream[1:4])

        elif sub_function == self.uds_server.SFID.REQUEST_ROUTINE_RESULT:
            if routine_id in self.routine_status:
                # Returning a dummy result
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RC, data_stream[1:4] + [0x01, 0x02, 0x03]
                )
            else:
                return self.uds_server.negative_response.report_negative_response(
                    self.uds_server.SID.RC, self.uds_server.NRC.REQUEST_OUT_OF_RANGE
                )

        else:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.RC, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )
