from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from py_uds_demo.core.server import UdsServer
from py_uds_demo.core.utils.helpers import split_integer_to_bytes


class ReadDataByIdentifier:
    """
    Handles Read Data By Identifier (0x22) service requests.

    What:
        This service is used to read data from the server (ECU), identified
        by a 2-byte Data Identifier (DID). It's one of the most common UDS
        services.

    Why:
        It provides a standardized way to read a wide variety of data, such
        as sensor values, configuration settings, part numbers, software
        versions, and more.

    How:
        The client sends a request with the SID 0x22 followed by one or more
        2-byte DIDs. The server responds with the SID 0x62, the requested
        DID(s), and the corresponding data.

    Real-world example:
        A workshop tool needs to verify the software version of an ECU. It
        sends a Read Data By Identifier request with the DID for the software
        version (e.g., 0xF188). The ECU responds with the version, which the
        tool then displays to the technician.

    Attributes:
        uds_server: The UDS server instance.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Read Data By Identifier request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) != 3:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.RDBI, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )
        did = (data_stream[1] << 8) | data_stream[2]
        match did:
            case self.uds_server.did.ACTIVE_DIAGNOSTIC_SESSION:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + [self.uds_server.diagnostic_session_control.active_session]
                )
            case self.uds_server.did.VEHICLE_IDENTIFICATION_NUMBER:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.vehicle_identification_number
                )
            case self.uds_server.did.MANUFACTURER_SPARE_PART_NUMBER:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.manufacturer_spare_part_number
                )
            case self.uds_server.did.MANUFACTURER_ECU_SOFTWARE_NUMBER:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.manufacturer_ecu_software_number
                )
            case self.uds_server.did.MANUFACTURER_ECU_SOFTWARE_VERSION:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.manufacturer_ecu_software_version
                )
            case self.uds_server.did.ECU_MANUFACTURING_DATE:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.ecu_manufacturing_date
                )
            case self.uds_server.did.ECU_SERIAL_NUMBER:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.ecu_serial_number
                )
            case self.uds_server.did.SUPPORTED_FUNCTIONAL_UNITS:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.supported_functional_units
                )
            case self.uds_server.did.SYSTEM_SUPPLIER_ECU_SOFTWARE_NUMBER:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.system_supplier_ecu_software_number
                )
            case self.uds_server.did.SYSTEM_SUPPLIER_ECU_SOFTWARE_VERSION:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.system_supplier_ecu_software_version
                )
            case self.uds_server.did.PROGRAMMING_DATE:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.programming_date
                )
            case self.uds_server.did.REPAIR_SHOP_CODE:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.repair_shop_code
                )
            case self.uds_server.did.EXHAUST_REGULATION_TYPE_APPROVAL_NUMBER:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.exhaust_regulation_type_approval_number
                )
            case self.uds_server.did.INSTALLATION_DATE:
                return self.uds_server.positive_response.report_positive_response(
                    self.uds_server.SID.RDBI, data_stream[1:3] + self.uds_server.memory.ecu_installation_date
                )
            case _:
                return self.uds_server.negative_response.report_negative_response(
                    self.uds_server.SID.RDBI, self.uds_server.NRC.REQUEST_OUT_OF_RANGE
                )


class ReadMemoryByAddress:
    """
    Handles Read Memory By Address (0x23) service requests.

    What:
        This service is used to read data from a specific memory address in
        the server (ECU).

    Why:
        It provides a low-level way to access the ECU's memory, which is
        useful for debugging, reverse engineering, or accessing data that
        is not available through a Data Identifier (DID).

    How:
        The client sends a request with the SID 0x23, followed by the memory
        address and the number of bytes to read. The server responds with
        the SID 0x63 and the requested data.

    Real-world example:
        A software developer is debugging a new feature and wants to inspect
        the value of a variable in real-time. They use the Read Memory By
        Address service to read the memory location where that variable is
        stored, helping them to understand its behavior.

    Attributes:
        uds_server: The UDS server instance.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Read Memory By Address request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) != 5:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.RMBA, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        address = (data_stream[1] << 24) | (data_stream[2] << 16) | (data_stream[3] << 8) | data_stream[4]

        if address not in self.uds_server.memory.memory_map:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.RMBA, self.uds_server.NRC.REQUEST_OUT_OF_RANGE
            )

        return self.uds_server.positive_response.report_positive_response(
            self.uds_server.SID.RMBA, self.uds_server.memory.memory_map[address]
        )


class ReadScalingDataByIdentifier:
    """
    Handles Read Scaling Data By Identifier (0x24) service requests.

    What:
        This service is used to retrieve the scaling information for a data
        value that is returned by the ReadDataByIdentifier service.

    Why:
        Some data values are transmitted as scaled integers to save space or
        for other reasons. This service provides the necessary information
        (e.g., a formula or a lookup table) to convert the raw integer value
        into a physical value (e.g., a floating-point number with a unit).

    How:
        The client sends a request with the SID 0x24 and a DID. The server
        responds with the scaling information for that DID.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Read Scaling Data By Identifier request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.RSDBI, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class ReadDataByPeriodicIdentifier:
    """
    Handles Read Data By Periodic Identifier (0x2A) service requests.

    What:
        This service is used to request that the server (ECU) periodically
        transmits the data values for one or more Data Identifiers (DIDs).

    Why:
        It's an efficient way to monitor data over time without the need for
        the client to continuously send requests. This is useful for data
        logging or for displaying live data on a diagnostic tool.

    How:
        The client sends a request with the SID 0x2A, specifying the DIDs
        to be read and the transmission rate. The server then starts sending
        the data periodically until instructed to stop.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Read Data By Periodic Identifier request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.RDBPI, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class DynamicallyDefineDataIdentifier:
    """
    Handles Dynamically Define Data Identifier (0x2C) service requests.

    What:
        This service allows a client to dynamically define a new Data
        Identifier (DID) at runtime. This new DID can be composed of data
        from other existing DIDs or from specific memory addresses.

    Why:
        It's useful when you need to read a combination of data that is not
        available in a single, predefined DID. Instead of sending multiple
        requests, you can create one dynamic DID to get all the data in a
        single response, which can be more efficient.

    How:
        The client sends a request with the SID 0x2C and the definition of
        the new DID, which includes the source DIDs or memory addresses.

    Note:
        This service is not fully implemented in this simulator.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Dynamically Define Data Identifier request.

        Args:
            data_stream: The request data stream.

        Returns:
            A negative response, as this service is not supported.
        """
        return self.uds_server.negative_response.report_negative_response(
            self.uds_server.SID.DDDI, self.uds_server.NRC.SERVICE_NOT_SUPPORTED
        )


class WriteDataByIdentifier:
    """
    Handles Write Data By Identifier (0x2E) service requests.

    What:
        This service is used to write data to the server (ECU) at a location
        specified by a Data Identifier (DID).

    Why:
        It's used to change the ECU's behavior or update its configuration.
        This can include things like setting a new speed limit, updating the
        VIN, or changing calibration values.

    How:
        The client sends a request with the SID 0x2E, the DID to be written,
        and the data to write. The server responds with the SID 0x6E and the
        DID that was written to confirm the operation.

    Real-world example:
        A car manufacturer wants to update the service date in the instrument
        cluster. A technician uses a diagnostic tool to send a Write Data By
        Identifier request with the DID for the service date and the new date.
        The instrument cluster then updates its display accordingly.

    Attributes:
        uds_server: The UDS server instance.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Write Data By Identifier request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) < 4:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.WDBI, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        did = (data_stream[1] << 8) | data_stream[2]

        if did not in self.uds_server.memory.writable_dids:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.WDBI, self.uds_server.NRC.REQUEST_OUT_OF_RANGE
            )

        data_to_write = data_stream[3:]
        self.uds_server.memory.did_data[did] = data_to_write

        return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.WDBI, data_stream[1:3])


class WriteMemoryByAddress:
    """
    Handles Write Memory By Address (0x3D) service requests.

    What:
        This service is used to write data to a specific memory address in
        the server (ECU).

    Why:
        It provides a low-level way to modify the ECU's memory, which is
        useful for debugging, applying patches, or writing data to memory
        locations that are not accessible through a Data Identifier (DID).

    How:
        The client sends a request with the SID 0x3D, the memory address,
        and the data to be written. The server responds with the SID 0x7D
        to confirm the operation.

    Real-world example:
        A developer needs to apply a small patch to the ECU's software
        without performing a full reflash. They can use the Write Memory By
        Address service to write the patched code directly into the
        specified memory locations.

    Attributes:
        uds_server: The UDS server instance.
    """
    def __init__(self, uds_server: 'UdsServer') -> None:
        self.uds_server: 'UdsServer' = uds_server

    def process_request(self, data_stream: list) -> list:
        """
        Processes a Write Memory By Address request.

        Args:
            data_stream: The request data stream.

        Returns:
            A list of bytes representing the response.
        """
        if len(data_stream) < 6:
            return self.uds_server.negative_response.report_negative_response(
                self.uds_server.SID.WMBA, self.uds_server.NRC.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT
            )

        address = (data_stream[1] << 24) | (data_stream[2] << 16) | (data_stream[3] << 8) | data_stream[4]
        data_to_write = data_stream[5:]
        self.uds_server.memory.memory_map[address] = data_to_write

        return self.uds_server.positive_response.report_positive_response(self.uds_server.SID.WMBA, [])
