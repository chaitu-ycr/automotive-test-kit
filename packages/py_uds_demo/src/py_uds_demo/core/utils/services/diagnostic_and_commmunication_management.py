import threading
import datetime
from time import sleep
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_uds_demo.core.server import UdsServer


class DiagnosticSessionControl:
    """
    Handles Diagnostic Session Control (0x10) service requests.

    What:
        This service is used to switch the server (ECU) to a specific
        diagnostic session. Each session can grant different levels of access
        to diagnostic services and data.

    Why:
        Different tasks require different security levels. For example, reading
        basic data might be allowed in a default session, but reprogramming
        the ECU would require switching to a programming session with higher
        security access.

    How:
        The client sends a request with the SID 0x10 followed by a single byte
        sub-function indicating the desired session.

    Real-world example:
        A technician uses a diagnostic tool to connect to a car. The tool
        starts in the default session, which allows reading error codes. To
        perform a software update, the tool requests to switch to the
        programming session. If the security checks pass, the ECU switches
        to the programming session, allowing the update to proceed.

    Attributes:
        uds_server: The UDS server instance.
        active_session: The currently active diagnostic session.
        supported_subfunctions: A list of supported sub-function identifiers.
        P2_HIGH (int): P2 timing parameter high byte.
        P2_LOW (int): P2 timing parameter low byte.
        P2_STAR_HIGH (int): P2* timing parameter high byte.
        P2_STAR_LOW (int): P2* timing parameter low byte.
        tester_present_active (bool): True if Tester Present is active.
        session_timeout (int): The timeout for non-default sessions in seconds.
    """
    def __init__(self, uds_server: 'UdsServer'):
        self.uds_server: 'UdsServer' = uds_server
        self.active_session = self.uds_server.SFID.DEFAULT_SESSION
        self.supported_subfunctions = [
            self.uds_server.SFID.DEFAULT_SESSION,
            self.uds_server.SFID.PROGRAMMING_SESSION,
            self.uds_server.SFID.EXTENDED_SESSION,
            self.uds_server.SFID.SAFETY_SYSTEM_DIAGNOSTIC_SESSION,
        ]
        # P2 = 50 ms
        self.P2_HIGH = 0x00
        self.P2_LOW = 0x32
        # P2* = 5000 ms
        self.P2_STAR_HIGH = 0x13
        self.P2_STAR_LOW = 0x88
        self.tester_present_active = False
        self.session_timeout = 5 # 5 seconds
        self.last_session_change_time = datetime.datetime.now()
        self.thread_event = threading.Event()
        self.session_thread = threading.Thread(target=self._start_active_session_timeout_thread, daemon=True)
        self.session_thread.start()

    def __del__(self):
        """Stops the session timeout thread."""
        self.thread_event.set()
        self.session_thread.join(1)

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Diagnostic Session Control request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) != 2:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.DSC, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )
        sfid = data_stream[1]
        if sfid not in self.supported_subfunctions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.DSC, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )

        self.active_session = sfid
        self.last_session_change_time = datetime.datetime.now()
        return self.uds_server.positive_response.report_positive_response(
            self.uds_server.SID.DSC, [sfid, self.P2_HIGH, self.P2_LOW, self.P2_STAR_HIGH, self.P2_STAR_LOW]
        )

    def _start_active_session_timeout_thread(self):
        """
        A thread that monitors the active session and reverts to the default
        session if no Tester Present message is received within the timeout.
        """
        while not self.thread_event.is_set():
            if self.tester_present_active:
                sleep(0.1)
                continue
            now = datetime.datetime.now()
            elapsed = (now - self.last_session_change_time).total_seconds()
            if self.active_session != self.uds_server.SFID.DEFAULT_SESSION and elapsed >= self.session_timeout:
                self.active_session = self.uds_server.SFID.DEFAULT_SESSION
                self.last_session_change_time = now
            sleep(0.1)


class EcuReset:
    """
    Handles ECU Reset (0x11) service requests.

    What:
        This service is used to restart an ECU. Different types of resets can
        be performed, such as a hard reset (simulating a power cycle) or a
        soft reset (re-initializing software).

    Why:
        An ECU reset is often necessary to recover an ECU from a faulty
        state, to apply new settings, or to complete a software update
        process.

    How:
        The client sends a request with the SID 0x11 followed by a single byte
        sub-function indicating the desired reset type.

    Real-world example:
        After successfully flashing a new firmware version to an ECU, a
        technician sends an ECU Reset request with the 'hardReset' sub-function.
        This forces the ECU to restart, loading the new firmware and
        completing the update process.

    Attributes:
        uds_server: The UDS server instance.
        supported_subfunctions: A list of supported sub-function identifiers.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.supported_subfunctions = [
            self.uds_server.SFID.HARD_RESET,
            self.uds_server.SFID.KEY_ON_OFF_RESET,
            self.uds_server.SFID.SOFT_RESET,
        ]

    def process_request(self, data_stream: list) -> list:
        """
        Processes an ECU Reset request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) != 2:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.ER, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )
        reset_type = data_stream[1]
        if reset_type not in self.supported_subfunctions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.ER, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )

        if (
            self.uds_server.diagnostic_session_control.active_session == self.uds_server.SFID.PROGRAMMING_SESSION
            and reset_type != self.uds_server.SFID.HARD_RESET
        ):
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.ER, self.uds_server.NRC.REQUEST_OUT_OF_RANGE
            )

        self.uds_server.diagnostic_session_control.active_session = self.uds_server.SFID.DEFAULT_SESSION
        self.uds_server.security_access.seed_sent = False
        self.uds_server.security_access.security_unlock_success = False
        return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.ER, [reset_type])


class SecurityAccess:
    """
    Handles Security Access (0x27) service requests.

    What:
        This service provides a security mechanism to protect certain services
        from unauthorized access. It uses a seed-and-key exchange to
        authenticate the client.

    Why:
        It's crucial to prevent unauthorized users from accessing critical
        ECU functions, such as flashing new software, changing the VIN, or
        modifying calibration data.

    How:
        The client requests a 'seed' from the ECU. Using a secret algorithm,
        the client calculates a 'key' from the seed and sends it back. If the
        key is correct, the ECU grants access to protected services.

    Real-world example:
        A manufacturer protects the engine's fuel map from being modified.
        To change the fuel map, a diagnostic tool must first use the Security
        Access service. The tool requests a seed, calculates the key, and
        sends it back. If successful, the tool can then use the Write Data
        By Identifier service to update the fuel map.

    Attributes:
        uds_server: The UDS server instance.
        seed_value: The last generated seed.
        seed_sent: True if a seed has been sent to the client.
        security_unlock_success: True if the ECU is unlocked.
        supported_subfunctions: A list of supported sub-function identifiers.
        supported_sessions: A list of sessions in which security access is allowed.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.seed_value = []
        self.seed_sent = False
        self.security_unlock_success = False
        self.supported_subfunctions = [
            self.uds_server.SFID.REQUEST_SEED,
            self.uds_server.SFID.SEND_KEY,
        ]
        self.supported_sessions = [
            self.uds_server.SFID.PROGRAMMING_SESSION,
            self.uds_server.SFID.EXTENDED_SESSION,
        ]

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Security Access request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) < 2:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.SA, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )
        if self.uds_server.diagnostic_session_control.active_session not in self.supported_sessions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.SA, self.uds_server.NRC.CONDITIONS_NOT_CORRECT
            )
        sfid = data_stream[1]
        if sfid not in self.supported_subfunctions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.SA, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )

        if (sfid % 2 == 0 and not self.seed_sent) or (sfid % 2 == 1 and self.seed_sent) or self.security_unlock_success:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.SA, self.uds_server.NRC.REQUEST_SEQUENCE_ERROR
            )

        if sfid % 2 == 1:
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.SA, [sfid] + self._get_seed())

        if len(data_stream) != 6:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.SA, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        if self._check_key(data_stream[2:]):
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.SA, [sfid])
        else:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.SA, self.uds_server.NRC.SECURITY_ACCESS_DENIED
            )

    def _get_seed(self) -> list:
        """Generates a random seed."""
        self.seed_value = [randint(0, 255) for _ in range(4)]
        self.seed_sent = True
        return self.seed_value

    def _check_key(self, key: list) -> bool:
        """
        Checks if the provided key is valid.

        Args:
            key: The key provided by the client.

        Returns:
            True if the key is valid, False otherwise.
        """
        internal_key = (
            (self.seed_value[0] << 24)
            | (self.seed_value[1] << 16)
            | (self.seed_value[2] << 8)
            | self.seed_value[3]
        ) | 0x11223344
        received_key = (
            (key[0] << 24)
            | (key[1] << 16)
            | (key[2] << 8)
            | key[3]
        )
        if internal_key == received_key:
            self.security_unlock_success = True
            return True
        return False


class CommunicationControl:
    """
    Handles Communication Control (0x28) service requests.

    What:
        This service is used to control the communication of the server (ECU)
        on the network. It can enable or disable the transmission and/or
        reception of certain types of messages.

    Why:
        It's useful for isolating an ECU during diagnostics or to prevent
        interference during sensitive operations like software flashing. For
        example, you can stop an ECU from sending messages that might
        disrupt other nodes on the network while you are reprogramming it.

    How:
        The client sends a request with the SID 0x28, a sub-function to
        specify the control type (e.g., enableRxAndTx, disableRx), and a
        parameter for the communication type (e.g., normal communication,
        network management).

    Real-world example:
        Before updating the firmware on an airbag control unit, a technician's
        tool sends a Communication Control request to disable the transmission
        of normal messages from that ECU. This prevents the ECU from sending
        any potentially conflicting messages during the update. Once the
        update is complete, the tool re-enables communication.

    Attributes:
        uds_server: The UDS server instance.
        supported_subfunctions: A list of supported sub-function identifiers.
        supported_communication_types: A list of supported communication types.
        supported_sessions: A list of sessions in which communication control is allowed.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.NORMAL_COMMUNICATION_MESSAGES = 0x01
        self.NETWORK_MANAGEMENT_MESSAGES = 0x01
        self.BOTH_TYPES = 0x01
        self.supported_subfunctions = [
            self.uds_server.SFID.ENABLE_RX_AND_TX,
            self.uds_server.SFID.ENABLE_RX_AND_DISABLE_TX,
            self.uds_server.SFID.DISABLE_RX_AND_ENABLE_TX,
            self.uds_server.SFID.DISABLE_RX_AND_TX,
        ]
        self.supported_communication_types = [
            self.NORMAL_COMMUNICATION_MESSAGES,
            self.NETWORK_MANAGEMENT_MESSAGES,
            self.BOTH_TYPES,
        ]
        self.supported_sessions = [
            self.uds_server.SFID.PROGRAMMING_SESSION,
            self.uds_server.SFID.EXTENDED_SESSION,
        ]

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Communication Control request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if not (len(data_stream) >= 3):
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CC, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )
        if self.uds_server.diagnostic_session_control.active_session not in self.supported_sessions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CC, self.uds_server.NRC.CONDITIONS_NOT_CORRECT
            )
        sfid = data_stream[1]
        if sfid not in self.supported_subfunctions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CC, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )

        communication_type = data_stream[2]
        if communication_type not in self.supported_communication_types:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CC, self.uds_server.NRC.REQUEST_OUT_OF_RANGE
            )

        return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.CC, data_stream[1:])


class TesterPresent:
    """
    Handles Tester Present (0x3E) service requests.

    What:
        This service is used to indicate to the server (ECU) that a client
        is still connected and that the current diagnostic session should
        remain active.

    Why:
        If there is no communication for a certain period, the ECU will
        automatically time out and return to the default diagnostic session.
        The Tester Present service prevents this from happening.

    How:
        The client periodically sends a request with the SID 0x3E. A sub-function
        can be used to either request a response from the server or suppress it.

    Real-world example:
        A technician is monitoring live data from a sensor, which requires
        the ECU to be in the extended diagnostic session. To prevent the
        session from timing out while they are observing the data, the
        diagnostic tool sends a Tester Present message every few seconds.

    Attributes:
        uds_server: The UDS server instance.
        tester_present_request_received: True if a Tester Present request has been received.
        supported_subfunctions: A list of supported sub-function identifiers.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.tester_present_request_received = False
        self.supported_subfunctions = [
            self.uds_server.SFID.ZERO_SUB_FUNCTION,
            self.uds_server.SFID.ZERO_SUB_FUNCTION_SUPRESS_RESPONSE,
        ]

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Tester Present request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response, or an empty list if the
            response is suppressed.
        """
        if len(data_stream) != 2:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.TP, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )
        sfid = data_stream[1]
        if sfid not in self.supported_subfunctions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.TP, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )

        self.tester_present_request_received = True
        if sfid == self.uds_server.SFID.ZERO_SUB_FUNCTION:
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.TP, data_stream[1:])
        else:
            return []  # Suppress response


class AccessTimingParameter:
    """
    Handles Access Timing Parameter (0x83) service requests.

    What:
        This service is used to read or write the communication timing
        parameters between the client and the server.

    Why:
        In certain situations, like on slow or high-latency networks, it may
        be necessary to adjust the default timing parameters (e.g., P2, P2*)
        to ensure reliable communication.

    How:
        The client can send a request to read the current timing parameters or
        to set new ones.

    Real-world example:
        A diagnostic tool is connected to an ECU over a wireless network, which
        has a higher latency than a direct wired connection. To prevent
        communication timeouts, the tool uses this service to extend the
        timing parameters, allowing more time for responses.

    Attributes:
        uds_server: The UDS server instance.
        supported_subfunctions: A list of supported sub-function identifiers.
        timing_parameters: A dictionary of timing parameters.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.supported_subfunctions = [
            self.uds_server.SFID.READ_EXTENDED_TIMING_PARAMETER_SET,
            self.uds_server.SFID.SET_TIMING_PARAMETERS_TO_DEFAULT_VALUE,
            self.uds_server.SFID.READ_CURRENTLY_ACTIVE_TIMING_PARAMETERS,
            self.uds_server.SFID.SET_TIMING_PARAMETERS_TO_GIVEN_VALUES,
        ]
        self.timing_parameters = {
            "P2_HIGH": 0x00,
            "P2_LOW": 0x32,
            "P2_STAR_HIGH": 0x13,
            "P2_STAR_LOW": 0x88,
        }

    def process_request(self, data_stream: list) -> list:
        """
        Processes an Access Timing Parameter request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) < 2:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.ATP, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        sfid = data_stream[1]
        if sfid not in self.supported_subfunctions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.ATP, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )

        if sfid == self.uds_server.SFID.READ_EXTENDED_TIMING_PARAMETER_SET or sfid == self.uds_server.SFID.READ_CURRENTLY_ACTIVE_TIMING_PARAMETERS:
            return self.uds_server.positive_response.report_positive_response(
                self.uds_server.SID.ATP, [sfid] + list(self.timing_parameters.values())
            )

        if sfid == self.uds_server.SFID.SET_TIMING_PARAMETERS_TO_DEFAULT_VALUE:
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.ATP, [sfid])

        if sfid == self.uds_server.SFID.SET_TIMING_PARAMETERS_TO_GIVEN_VALUES:
            if len(data_stream) != 6:
                return self.uds_server.negative_response.report_negative_response(
                    self.uds_server.SID.ATP, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
                )

            self.timing_parameters["P2_HIGH"] = data_stream[2]
            self.timing_parameters["P2_LOW"] = data_stream[3]
            self.timing_parameters["P2_STAR_HIGH"] = data_stream[4]
            self.timing_parameters["P2_STAR_LOW"] = data_stream[5]
            return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.ATP, [sfid])

        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.ATP, self.uds_server.NRC.REQUEST_OUT_OF_RANGE
        )


class SecuredDataTransmission:
    """
    Handles Secured Data Transmission (0x84) service requests.

    What:
        This service is used to transmit data securely between the client and
        the server, providing cryptographic protection for the data.

    Why:
        It's used when sensitive data needs to be exchanged over a potentially
        insecure network, ensuring confidentiality and integrity.

    How:
        The implementation details, including the cryptographic algorithms,
        are typically manufacturer-specific.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Secured Data Transmission request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.SDT, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class ControlDtcSetting:
    """
    Handles Control DTC Setting (0x85) service requests.

    What:
        This service is used to enable or disable the setting of Diagnostic
        Trouble Codes (DTCs) in the server (ECU).

    Why:
        During maintenance or testing, some actions might trigger false DTCs.
        This service allows a client to temporarily disable DTC reporting to
        avoid filling the fault memory with irrelevant codes.

    How:
        The client sends a request with the SID 0x85 and a sub-function to
        either enable (0x01) or disable (0x02) DTC setting.

    Real-world example:
        A technician is replacing a sensor. To prevent the ECU from storing
        a DTC for the disconnected sensor during the replacement process,
        they first use this service to disable DTC setting. After the new
        sensor is installed, they re-enable it.

    Attributes:
        uds_server: The UDS server instance.
        supported_subfunctions: A list of supported sub-function identifiers.
        supported_sessions: A list of sessions in which this service is allowed.
        dtc_setting: The current DTC setting (ON or OFF).
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.supported_subfunctions = [
            self.uds_server.SFID.ON,
            self.uds_server.SFID.OFF,
        ]
        self.supported_sessions = [
            self.uds_server.SFID.PROGRAMMING_SESSION,
            self.uds_server.SFID.EXTENDED_SESSION,
        ]
        self.dtc_setting = self.uds_server.SFID.ON

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Control DTC Setting request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) != 2:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CDTCS, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )
        if self.uds_server.diagnostic_session_control.active_session not in self.supported_sessions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CDTCS, self.uds_server.NRC.CONDITIONS_NOT_CORRECT
            )
        sfid = data_stream[1]
        if sfid not in self.supported_subfunctions:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.CDTCS, self.uds_server.NRC.SUB_FUNCTION_NOT_SUPPORTED
            )

        self.dtc_setting = sfid
        return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.CDTCS, data_stream[1:])


class ResponseOnEvent:
    """
    Handles Response On Event (0x86) service requests.

    What:
        This service allows a client to request that the server (ECU)
        automatically sends a response when a specific event occurs, instead
        of the client having to poll for it.

    Why:
        It's useful for monitoring real-time events without the overhead of
        continuous polling. For example, a client can be notified immediately
        when a DTC is set or a sensor value crosses a certain threshold.

    How:
        The client sends a request to register an event (e.g., onDtcStatusChange)
        and specifies the response that the server should send when that event
        occurs.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.supported_subfunctions = [
            self.uds_server.SFID.DO_NOT_STORE_EVENT,
            self.uds_server.SFID.STORE_EVENT,
            self.uds_server.SFID.STOP_RESPONSE_ON_EVENT,
            self.uds_server.SFID.ON_DTC_STATUS_CHANGE,
            self.uds_server.SFID.ON_TIMER_INTERRUPT,
            self.uds_server.SFID.ON_CHANGE_OF_DATA_IDENTIFIER,
            self.uds_server.SFID.REPORT_ACTIVATED_EVENTS,
            self.uds_server.SFID.START_RESPONSE_ON_EVENT,
            self.uds_server.SFID.CLEAR_RESPONSE_ON_EVENT,
            self.uds_server.SFID.ON_COMPARISON_OF_VALUE,
        ]

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Response On Event request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.ROE, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class LinkControl:
    """
    Handles Link Control (0x87) service requests.

    What:
        This service is used to control the baud rate of the communication
        link between the client and the server.

    Why:
        It can be used to switch to a higher baud rate for faster data
        transfer, which is particularly useful for time-consuming operations
        like software flashing.

    How:
        The process typically involves the client first verifying that the
        server can support the new baud rate and then sending a command to
        transition to it.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server
        self.supported_subfunctions = [
            self.uds_server.SFID.VERIFY_MODE_TRANSITION_WITH_FIXED_PARAMETER,
            self.uds_server.SFID.VERIFY_MODE_TRANSITION_WITH_SPECIFIC_PARAMETER,
            self.uds_server.SFID.TRANSITION_MODE,
        ]

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Link Control request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.LC, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )
