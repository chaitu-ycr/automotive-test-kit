from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from py_uds_demo.core.server import UdsServer


class RequestDownload:
    """
    Handles Request Download (0x34) service requests.

    What:
        This service is used to initiate a data download from the client to
        the server (ECU). It's the first step in the process of flashing new
        software or writing a large block of data to the ECU.

    Why:
        It prepares the ECU to receive data, and the ECU can specify the
        maximum size of the data blocks it can accept at a time.

    How:
        The client sends a request with the SID 0x34, the memory address
        where the data should be stored, and the total size of the data.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Request Download request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.RD, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class RequestUpload:
    """
    Handles Request Upload (0x35) service requests.

    What:
        This service is used to initiate a data upload from the server (ECU)
        to the client.

    Why:
        It's used to read large blocks of data from the ECU, such as log
        files, calibration data, or the entire memory content.

    How:
        The client sends a request with the SID 0x35, the memory address
        of the data to be uploaded, and the size of the data.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Request Upload request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.RU, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class TransferData:
    """
    Handles Transfer Data (0x36) service requests.

    What:
        This service is used to transfer data blocks between the client and
        the server during an upload or download operation.

    Why:
        It's the workhorse of the data transfer process, responsible for
        moving the actual data in chunks.

    How:
        After a download or upload is initiated, the client (for downloads)
        or server (for uploads) sends a sequence of Transfer Data requests,
        each containing a block of data.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Transfer Data request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.TD, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class RequestTransferExit:
    """
    Handles Request Transfer Exit (0x37) service requests.

    What:
        This service is used to terminate a data transfer sequence.

    Why:
        It signals the end of the upload or download process, allowing the
        server to perform any necessary cleanup or verification.

    How:
        The client sends a request with the SID 0x37 to indicate that the
        transfer is complete.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Request Transfer Exit request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.RTE, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class RequestFileTransfer:
    """
    Handles Request File Transfer (0x38) service requests.

    What:
        This service provides a more advanced and flexible way to transfer
        files between the client and the server, often with file-system-like
        operations.

    Why:
        It's designed to be more powerful than the older upload/download
        services, supporting more complex use cases.

    How:
        The specifics are complex and can vary between implementations.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Request File Transfer request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.RFT, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )
