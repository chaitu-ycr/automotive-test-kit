import os
import sys
import logging

from py_uds_demo.core.utils.services import diagnostic_and_commmunication_management
from py_uds_demo.core.utils.services import data_transmission
from py_uds_demo.core.utils.services import stored_data_transmission
from py_uds_demo.core.utils.services import input_output_contol
from py_uds_demo.core.utils.services import remote_activation_of_routine
from py_uds_demo.core.utils.services import upload_download
from py_uds_demo.core.utils.responses import PositiveResponse, NegativeResponse
from py_uds_demo.core.utils.helpers import Sid, Sfid, Nrc, Did, Memory


class UdsServer:
    """
    Implements the UDS server functionality.

    This class initializes all supported UDS services, constants, and response
    handlers. It provides a method to process incoming diagnostic requests and
    route them to the appropriate service handler.

    Attributes:
        DEFAULT_LOG_FILE (str): The default path for the log file.
        logger (logging.Logger): The logger instance for the server.
        SID (Sid): Service identifiers.
        SFID (Sfid): Sub-function identifiers.
        NRC (Nrc): Negative response codes.
        did (Did): Diagnostic identifiers.
        memory (Memory): Memory map and data.
        positive_response (PositiveResponse): Handler for positive responses.
        negative_response (NegativeResponse): Handler for negative responses.
        diagnostic_and_commmunication_management: Diagnostic and communication management service handler.
        data_transmission: Data transmission service handler.
        stored_data_transmission: Stored data transmission service handler.
        input_output_contol: Input/output control service handler.
        remote_activation_of_routine: Remote activation of routine service handler.
        upload_download: Upload/download service handler.
    """
    def __init__(self):
        # Logger
        self.DEFAULT_LOG_FILE = "_temp/logs/uds_simulator.log"
        self.logger = self._initialize_logger()
        # Constants
        self.SID = Sid()
        self.SFID = Sfid()
        self.NRC = Nrc()
        self.did = Did()
        self.memory = Memory()
        # Responses
        self.positive_response = PositiveResponse()
        self.negative_response = NegativeResponse()
        # Diagnostic and communication management
        self.diagnostic_session_control = diagnostic_and_commmunication_management.DiagnosticSessionControl(self)
        self.ecu_reset = diagnostic_and_commmunication_management.EcuReset(self)
        self.security_access = diagnostic_and_commmunication_management.SecurityAccess(self)
        self.communication_control = diagnostic_and_commmunication_management.CommunicationControl(self)
        self.tester_present = diagnostic_and_commmunication_management.TesterPresent(self)
        self.access_timing_parameter = diagnostic_and_commmunication_management.AccessTimingParameter(self)
        self.secured_data_transmission = diagnostic_and_commmunication_management.SecuredDataTransmission(self)
        self.control_dtc_setting = diagnostic_and_commmunication_management.ControlDtcSetting(self)
        self.response_on_event = diagnostic_and_commmunication_management.ResponseOnEvent(self)
        self.link_control = diagnostic_and_commmunication_management.LinkControl(self)
        # Data transmission
        self.read_data_by_identifier = data_transmission.ReadDataByIdentifier(self)
        self.read_memory_by_address = data_transmission.ReadMemoryByAddress(self)
        self.read_scaling_data_by_identifier = data_transmission.ReadScalingDataByIdentifier(self)
        self.read_data_by_periodic_identifier = data_transmission.ReadDataByPeriodicIdentifier(self)
        self.dynamically_define_data_identifier = data_transmission.DynamicallyDefineDataIdentifier(self)
        self.write_data_by_identifier = data_transmission.WriteDataByIdentifier(self)
        self.write_memory_by_address = data_transmission.WriteMemoryByAddress(self)
        # Stored data transmission
        self.clear_diagnostic_information = stored_data_transmission.ClearDiagnosticInformation(self)
        self.read_dtc_information = stored_data_transmission.ReadDtcInformation(self)
        # Input Output control
        self.input_output_control_by_identifier = input_output_contol.InputOutputControlByIdentifier(self)
        # Remote activation of routine
        self.routine_control = remote_activation_of_routine.RoutineControl(self)
        # Upload download
        self.request_download = upload_download.RequestDownload(self)
        self.request_upload = upload_download.RequestUpload(self)
        self.transfer_data = upload_download.TransferData(self)
        self.request_transfer_exit = upload_download.RequestTransferExit(self)
        self.request_file_transfer = upload_download.RequestFileTransfer(self)
        # Service map
        self.service_map = {
            self.SID.DIAGNOSTIC_SESSION_CONTROL: self.diagnostic_session_control,
            self.SID.ECU_RESET: self.ecu_reset,
            self.SID.SECURITY_ACCESS: self.security_access,
            self.SID.COMMUNICATION_CONTROL: self.communication_control,
            self.SID.TESTER_PRESENT: self.tester_present,
            self.SID.ACCESS_TIMING_PARAMETER: self.access_timing_parameter,
            self.SID.SECURED_DATA_TRANSMISSION: self.secured_data_transmission,
            self.SID.CONTROL_DTC_SETTING: self.control_dtc_setting,
            self.SID.RESPONSE_ON_EVENT: self.response_on_event,
            self.SID.LINK_CONTROL: self.link_control,
            self.SID.READ_DATA_BY_IDENTIFIER: self.read_data_by_identifier,
            self.SID.READ_MEMORY_BY_ADDRESS: self.read_memory_by_address,
            self.SID.READ_SCALING_DATA_BY_IDENTIFIER: self.read_scaling_data_by_identifier,
            self.SID.READ_DATA_BY_PERIODIC_IDENTIFIER: self.read_data_by_periodic_identifier,
            self.SID.DYNAMICALLY_DEFINE_DATA_IDENTIFIER: self.dynamically_define_data_identifier,
            self.SID.WRITE_DATA_BY_IDENTIFIER: self.write_data_by_identifier,
            self.SID.WRITE_MEMORY_BY_ADDRESS: self.write_memory_by_address,
            self.SID.CLEAR_DIAGNOSTIC_INFORMATION: self.clear_diagnostic_information,
            self.SID.READ_DTC_INFORMATION: self.read_dtc_information,
            self.SID.INPUT_OUTPUT_CONTROL_BY_IDENTIFIER: self.input_output_control_by_identifier,
            self.SID.ROUTINE_CONTROL: self.routine_control,
            self.SID.REQUEST_DOWNLOAD: self.request_download,
            self.SID.REQUEST_UPLOAD: self.request_upload,
            self.SID.TRANSFER_DATA: self.transfer_data,
            self.SID.REQUEST_TRANSFER_EXIT: self.request_transfer_exit,
            self.SID.REQUEST_FILE_TRANSFER: self.request_file_transfer,
        }

    def _initialize_logger(self):
        """
        Initializes the logger for the UDS server.

        Sets up the logging configuration to output messages to both the console
        and a file.

        Returns:
            logging.Logger: The configured logger instance.
        """
        os.makedirs(os.path.dirname(self.DEFAULT_LOG_FILE), exist_ok=True)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        fmt = "%(asctime)s [UDS_SIM_UI] [%(levelname)-4.8s] %(message)s"
        if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
            file_handler = logging.FileHandler(self.DEFAULT_LOG_FILE, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(fmt))
            logger.addHandler(file_handler)
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(logging.Formatter(fmt))
            logger.addHandler(console_handler)
        logger.propagate = True
        return logger

    @property
    def supported_services(self) -> list:
        """
        Returns a list of all supported UDS service identifiers (SIDs).

        Returns:
            A list of integers representing the supported SIDs.
        """
        return list(self.SID.__dict__.values())

    def process_request(self, data_stream: list) -> list:
        """
        Processes an incoming UDS request and returns a response.

        Args:
            data_stream: A list of integers representing the incoming
                diagnostic request bytes.

        Returns:
            A list of integers representing the response to the request.
        """
        if not data_stream:
            return self.negative_response.report_negative_response(0x00, self.NRC.GENERAL_REJECT)
        sid = data_stream[0]
        match sid:
            # Diagnostic and communication management
            case self.SID.DIAGNOSTIC_SESSION_CONTROL:
                return self.diagnostic_session_control.process_request(data_stream)
            case self.SID.ECU_RESET:
                return self.ecu_reset.process_request(data_stream)
            case self.SID.SECURITY_ACCESS:
                return self.security_access.process_request(data_stream)
            case self.SID.COMMUNICATION_CONTROL:
                return self.communication_control.process_request(data_stream)
            case self.SID.TESTER_PRESENT:
                return self.tester_present.process_request(data_stream)
            case self.SID.ACCESS_TIMING_PARAMETER:
                return self.access_timing_parameter.process_request(data_stream)
            case self.SID.SECURED_DATA_TRANSMISSION:
                return self.secured_data_transmission.process_request(data_stream)
            case self.SID.CONTROL_DTC_SETTING:
                return self.control_dtc_setting.process_request(data_stream)
            case self.SID.RESPONSE_ON_EVENT:
                return self.response_on_event.process_request(data_stream)
            case self.SID.LINK_CONTROL:
                return self.link_control.process_request(data_stream)
            # Data transmission
            case self.SID.READ_DATA_BY_IDENTIFIER:
                return self.read_data_by_identifier.process_request(data_stream)
            case self.SID.READ_MEMORY_BY_ADDRESS:
                return self.read_memory_by_address.process_request(data_stream)
            case self.SID.READ_SCALING_DATA_BY_IDENTIFIER:
                return self.read_scaling_data_by_identifier.process_request(data_stream)
            case self.SID.READ_DATA_BY_PERIODIC_IDENTIFIER:
                return self.read_data_by_periodic_identifier.process_request(data_stream)
            case self.SID.DYNAMICALLY_DEFINE_DATA_IDENTIFIER:
                return self.dynamically_define_data_identifier.process_request(data_stream)
            case self.SID.WRITE_DATA_BY_IDENTIFIER:
                return self.write_data_by_identifier.process_request(data_stream)
            case self.SID.WRITE_MEMORY_BY_ADDRESS:
                return self.write_memory_by_address.process_request(data_stream)
            # Stored data transmission
            case self.SID.CLEAR_DIAGNOSTIC_INFORMATION:
                return self.clear_diagnostic_information.process_request(data_stream)
            case self.SID.READ_DTC_INFORMATION:
                return self.read_dtc_information.process_request(data_stream)
            # Input Output control
            case self.SID.INPUT_OUTPUT_CONTROL_BY_IDENTIFIER:
                return self.input_output_control_by_identifier.process_request(data_stream)
            # Remote activation of routine
            case self.SID.ROUTINE_CONTROL:
                return self.routine_control.process_request(data_stream)
            # Upload download
            case self.SID.REQUEST_DOWNLOAD:
                return self.request_download.process_request(data_stream)
            case self.SID.REQUEST_UPLOAD:
                return self.request_upload.process_request(data_stream)
            case self.SID.TRANSFER_DATA:
                return self.transfer_data.process_request(data_stream)
            case self.SID.REQUEST_TRANSFER_EXIT:
                return self.request_transfer_exit.process_request(data_stream)
            case self.SID.REQUEST_FILE_TRANSFER:
                return self.request_file_transfer.process_request(data_stream)
            # Negative Response
            case _:
                return self.negative_response.report_negative_response(sid, self.NRC.SERVICE_NOT_SUPPORTED)
