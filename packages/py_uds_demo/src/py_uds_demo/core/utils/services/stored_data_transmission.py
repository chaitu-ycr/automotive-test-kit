from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from py_uds_demo.core.server import UdsServer


class ClearDiagnosticInformation:
    """
    Handles Clear Diagnostic Information (0x14) service requests.

    What:
        This service is used to clear Diagnostic Trouble Codes (DTCs) from
        the server's (ECU's) memory.

    Why:
        After a vehicle has been repaired, the stored DTCs related to the
        fixed issue need to be cleared. This service provides the means to
        do so.

    How:
        The client sends a request with the SID 0x14, followed by a 3-byte
        groupOfDTC parameter, which specifies which DTCs to clear. A value
        of 0xFFFFFF is typically used to clear all DTCs.

    Real-world example:
        A "Check Engine" light is on. A technician reads the DTCs and finds
        a code for a faulty sensor. After replacing the sensor, the technician
        uses this service to clear the DTC, which turns off the light.

    Attributes:
        uds_server: The UDS server instance.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Clear Diagnostic Information request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if self.uds_server.control_dtc_setting.dtc_setting == self.uds_server.SFID.OFF:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CDTCI, self.uds_server.NRC.CONDITIONS_NOT_CORRECT
            )

        self.uds_server.memory.dtcs = []
        return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.CDTCI, [])


class ReadDtcInformation:
    """
    Handles Read DTC Information (0x19) service requests.

    What:
        This service is used to read Diagnostic Trouble Codes (DTCs) and
        related data from the server's (ECU's) memory.

    Why:
        It's the primary service for diagnosing vehicle problems. By reading
        DTCs, a technician can identify the system or component that is
        faulty. It also allows reading additional data, like "freeze frames"
        or "snapshot data," which is a snapshot of the vehicle's state at
        the time the fault occurred.

    How:
        The client sends a request with the SID 0x19 and a sub-function that
        specifies what information to read (e.g., number of DTCs, DTCs by
        status mask, snapshot data).

    Real-world example:
        A technician connects a diagnostic tool to a car with the "Check
        Engine" light on. The tool uses this service with the
        'reportDTCByStatusMask' sub-function to retrieve all active DTCs.
        The tool might then use another sub-function to read the snapshot
        data for a specific DTC to get more context about when the fault
        occurred.

    Attributes:
        uds_server: The UDS server instance.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Read DTC Information request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) < 2:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.RDTCI, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        sub_function = data_stream[1]

        if sub_function == self.uds_server.SFID.REPORT_NUMBER_OF_DTC_BY_STATUS_MASK:
            if len(data_stream) != 3:
                return self.uds_server.negative_response.report_negative_response(
                    self.uds_server.SID.RDTCI, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
                )
            status_mask = data_stream[2]
            # In this simulation, we'll just count all DTCs regardless of status mask
            num_dtcs = len(self.uds_server.memory.dtcs)
            return self.uds_server.positive_response.report_positive_response(
                self.uds_server.SID.RDTCI, [sub_function, status_mask, 0x01, num_dtcs]
            )

        elif sub_function == self.uds_server.SFID.REPORT_DTC_BY_STATUS_MASK:
            if len(data_stream) != 3:
                return self.uds_server.negative_response.report_negative_response(
                    self.uds_server.SID.RDTCI, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
                )
            status_mask = data_stream[2]
            # In this simulation, we'll return all DTCs regardless of status mask
            response_data = [sub_function, status_mask]
            for dtc in self.uds_server.memory.dtcs:
                response_data.extend(dtc)
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.RDTCI, response_data)

        else:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.RDTCI, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )
