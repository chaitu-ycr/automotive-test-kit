def split_integer_to_bytes(value: int) -> list[int]:
    """Splits an integer into a list of bytes (little-endian).

    Args:
        value: The integer to split.

    Returns:
        A list of integers, where each integer is a byte.
    """
    return [(value >> (i * 8)) & 0xFF for i in range((value.bit_length() + 7) // 8)]


class Sid:
    """Service Identifiers (SIDs) for UDS.

    This class contains constants for all service identifiers as defined in
    the ISO 14229 standard. Each SID has a long name and a short alias.

    See Also:
        ISO 14229
    """
    def __init__(self) -> None:
        # Diagnostic and communication management
        self.DIAGNOSTIC_SESSION_CONTROL = self.DSC = 0x10
        self.ECU_RESET = self.ER = 0x11
        self.SECURITY_ACCESS = self.SA = 0x27
        self.COMMUNICATION_CONTROL = self.CC = 0X28
        self.TESTER_PRESENT = self.TP = 0x3E
        self.ACCESS_TIMING_PARAMETER = self.ATP = 0x83
        self.SECURED_DATA_TRANSMISSION = self.SDT = 0x84
        self.CONTROL_DTC_SETTING = self.CDTCS = 0x85
        self.RESPONSE_ON_EVENT = self.ROE = 0x86
        self.LINK_CONTROL = self.LC = 0x87
        # Data transmission
        self.READ_DATA_BY_IDENTIFIER = self.RDBI = 0x22
        self.READ_MEMORY_BY_ADDRESS = self.RMBA = 0x23
        self.READ_SCALING_DATA_BY_IDENTIFIER = self.RSDBI = 0x24
        self.READ_DATA_BY_PERIODIC_IDENTIFIER = self.RDBPI = 0x2A
        self.DYNAMICALLY_DEFINE_DATA_IDENTIFIER = self.DDDI = 0x2C
        self.WRITE_DATA_BY_IDENTIFIER = self.WDBI = 0x2E
        self.WRITE_MEMORY_BY_ADDRESS = self.WMBA = 0x3D
        # Stored data transmission
        self.CLEAR_DIAGNOSTIC_INFORMATION = self.CDTCI = 0x14
        self.READ_DTC_INFORMATION = self.RDTCI = 0x19
        # Input Output control
        self.INPUT_OUTPUT_CONTROL_BY_IDENTIFIER = self.IOCBI = 0x2F
        # Remote activation of routine
        self.ROUTINE_CONTROL = self.RC = 0x31
        # Upload download
        self.REQUEST_DOWNLOAD = self.RD = 0x34
        self.REQUEST_UPLOAD = self.RU = 0x35
        self.TRANSFER_DATA = self.TD = 0x36
        self.REQUEST_TRANSFER_EXIT = self.RTE = 0x37
        self.REQUEST_FILE_TRANSFER = self.RFT = 0x38
        # Negative Response
        self.NEGATIVE_RESPONSE = self.NR = 0x7F


class Sfid:
    """Sub-function Identifiers (SFIDs) for UDS.

    This class contains constants for all sub-function identifiers as defined
    in the ISO 14229 standard. Each SFID has a long name and a short alias.

    See Also:
        ISO 14229
    """
    def __init__(self) -> None:
        # diagnostic_session_control
        self.DEFAULT_SESSION = self.DS = 0x01
        self.PROGRAMMING_SESSION = self.PRGS = 0x02
        self.EXTENDED_SESSION = self.EXTDS = 0x03
        self.SAFETY_SYSTEM_DIAGNOSTIC_SESSION = self.SSDS = 0x04
        # ecu_reset
        self.HARD_RESET = self.HR = 0x01
        self.KEY_ON_OFF_RESET = self.KOFFONR = 0x02
        self.SOFT_RESET = self.SR = 0x03
        self.ENABLE_RAPID_POWER_SHUTDOWN = self.ERPSD = 0x04
        self.DISABLE_RAPID_POWER_SHUTDOWN = self.DRPSD = 0x05
        # security_access
        self.REQUEST_SEED = self.RSD = 0x01
        self.SEND_KEY = self.SK = 0x02
        # communication_control
        self.ENABLE_RX_AND_TX = self.ERXTX = 0x00
        self.ENABLE_RX_AND_DISABLE_TX = self.ERXDTX = 0x01
        self.DISABLE_RX_AND_ENABLE_TX = self.DRXETX = 0x02
        self.DISABLE_RX_AND_TX = self.DRXTX = 0x03
        self.ENABLE_RX_AND_DISABLE_TX_WITH_ENHANCED_ADDRESS_INFORMATION = self.ERXDTXWEAI = 0x04
        self.ENABLE_RX_AND_TX_WITH_ENHANCED_ADDRESS_INFORMATION = self.ERXTXWEAI = 0x05
        # tester_present
        self.ZERO_SUB_FUNCTION = self.ZSUBF = 0x00
        self.ZERO_SUB_FUNCTION_SUPRESS_RESPONSE = 0x80
        # access_timing_parameter
        self.READ_EXTENDED_TIMING_PARAMETER_SET = self.RETPS = 0x01
        self.SET_TIMING_PARAMETERS_TO_DEFAULT_VALUE = self.STPTDV = 0x02
        self.READ_CURRENTLY_ACTIVE_TIMING_PARAMETERS = self.RCATP = 0x03
        self.SET_TIMING_PARAMETERS_TO_GIVEN_VALUES = self.STPTGV = 0x04
        # control_dtc_setting
        self.ON = self.ON = 0x01
        self.OFF = self.OFF = 0x02
        # response_on_event
        self.DO_NOT_STORE_EVENT = self.DNSE = 0x00
        self.STORE_EVENT = self.SE = 0x01
        self.STOP_RESPONSE_ON_EVENT = self.STPROE = 0x00
        self.ON_DTC_STATUS_CHANGE = self.ONDTCS = 0x01
        self.ON_TIMER_INTERRUPT = self.OTI = 0x02
        self.ON_CHANGE_OF_DATA_IDENTIFIER = self.OCODID = 0x03
        self.REPORT_ACTIVATED_EVENTS = self.RAE = 0x04
        self.START_RESPONSE_ON_EVENT = self.STRTROE = 0x05
        self.CLEAR_RESPONSE_ON_EVENT = self.CLRROE = 0x06
        self.ON_COMPARISON_OF_VALUE = self.OCOV = 0x07
        # link_control
        self.VERIFY_MODE_TRANSITION_WITH_FIXED_PARAMETER = self.VMTWFP = 0x01
        self.VERIFY_MODE_TRANSITION_WITH_SPECIFIC_PARAMETER = self.VMTWSP = 0x02
        self.TRANSITION_MODE = self.TM = 0x03
        # dynamically_define_data_identifier
        self.DEFINE_BY_IDENTIFIER = self.DBID = 0x01
        self.DEFINE_BY_MEMORY_ADDRESS = self.DBMA = 0x02
        self.CLEAR_DYNAMICALLY_DEFINED_DATA_IDENTIFIER = self.CDDDID = 0x03
        # read_dtc_information
        self.REPORT_NUMBER_OF_DTC_BY_STATUS_MASK = self.RNODTCBSM = 0x01
        self.REPORT_DTC_BY_STATUS_MASK = self.RDTCBSM = 0x02
        self.REPORT_DTC_SNAPSHOT_IDENTIFICATION = self.RDTCSSI = 0x03
        self.REPORT_DTC_SNAPSHOT_RECORD_BY_DTC_NUMBER = self.RDTCSSBDTC = 0x04
        self.READ_DTC_STORED_DATA_BY_RECORD_NUMBER = self.RDTCSDBRN = 0x05
        self.REPORT_DTC_EXT_DATA_RECORD_BY_DTC_NUMBER = self.RDTCEDRBDN = 0x06
        self.REPORT_NUMBER_OF_DTC_BY_SEVERITY_MASK_RECORD = self.RNODTCBSMR = 0x07
        self.REPORT_DTC_BY_SEVERITY_MASK_RECORD = self.RDTCBSMR = 0x08
        self.REPORT_SEVERITY_INFORMATION_OF_DTC = self.RSIODTC = 0x09
        self.REPORT_MIRROR_MEMORY_DTC_EXT_DATA_RECORD_BY_DTC_NUMBER = self.RMDEDRBDN = 0x10
        self.REPORT_SUPPORTED_DTC = self.RSUPDTC = 0x0A
        self.REPORT_FIRST_TEST_FAILED_DTC = self.RFTFDTC = 0x0B
        self.REPORT_FIRST_CONFIRMED_DTC = self.RFCDTC = 0x0C
        self.REPORT_MOST_RECENT_TEST_FAILED_DTC = self.RMRTFDTC = 0x0D
        self.REPORT_MOST_RECENT_CONFIRMED_DTC = self.RMRCDTC = 0x0E
        self.REPORT_MIRROR_MEMORY_DTC_BY_STATUS_MASK = self.RMMDTCBSM = 0x0F
        self.REPORT_NUMBER_OF_MIRROR_MEMORY_DTC_BY_STATUS_MASK = self.RNOMMDTCBSM = 0x11
        self.REPORT_NUMBER_OF_EMISSION_OBD_DTC_BY_STATUS_MASK = self.RNOOEBDDTCBSM = 0x12
        self.REPORT_EMISSION_OBD_DTC_BY_STATUS_MASK = self.ROBDDTCBSM = 0x13
        self.REPORT_DTC_FAULT_DETECTION_COUNTER = self.RDTCFDC = 0x14
        self.REPORT_DTC_WITH_PERMANENT_STATUS = self.RDTCWPS = 0x15
        self.REPORT_DTC_EXT_DATA_RECORD_BY_RECORD_NUMBER = self.RDTCEDRBR = 0x16
        self.REPORT_USER_DEF_MEMORY_DTC_BY_STATUS_MASK = self.RUDMDTCBSM = 0x17
        self.REPORT_USER_DEF_MEMORY_DTC_SNAPSHOT_RECORD_BY_DTC_NUMBER = self.RUDMDTCSSBDTC = 0x18
        self.REPORT_USER_DEF_MEMORY_DTC_EXT_DATA_RECORD_BY_DTC_NUMBER = self.RUDMDTCEDRBDN = 0x19
        self.REPORT_WWH_OBD_DTC_BY_MASK_RECORD = self.ROBDDTCBMR = 0x42
        self.REPORT_WWH_OBD_DTC_WITH_PERMANENT_STATUS = self.RWWHOBDDTCWPS = 0x55
        self.START_ROUTINE = self.STR = 0x01
        self.STOP_ROUTINE = self.STPR = 0x02
        self.REQUEST_ROUTINE_RESULT = self.RRR = 0x03


class Nrc:
    """Negative Response Codes (NRCs) for UDS.

    This class contains constants for all negative response codes as defined
    in the ISO 14229 standard. Each NRC has a long name and a short alias.

    See Also:
        ISO 14229
    """
    def __init__(self) -> None:
        self.GENERAL_REJECT = self.GR = 0x10
        self.SERVICE_NOT_SUPPORTED = self.SNS = 0x11
        self.SUB_FUNCTION_NOT_SUPPORTED = self.SFNS = 0x12
        self.INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT = self.IMLOIF = 0x13
        self.RESPONSE_TOO_LONG = self.RTL = 0x14
        self.BUSY_REPEAT_REQUEST = self.BRR = 0x21
        self.CONDITIONS_NOT_CORRECT = self.CNC = 0x22
        self.REQUEST_SEQUENCE_ERROR = self.RSE = 0x24
        self.NO_RESPONSE_FROM_SUBNET_COMPONENT = self.NRFSC = 0x25
        self.FAILURE_PREVENTS_EXECUTION_OF_REQUESTED_ACTION = self.FPEORA = 0x26
        self.REQUEST_OUT_OF_RANGE = self.ROOR = 0x31
        self.SECURITY_ACCESS_DENIED = self.SAD = 0x33
        self.INVALID_KEY = self.IK = 0x35
        self.EXCEEDED_NUMBER_OF_ATTEMPTS = self.ENOA = 0x36
        self.REQUIRED_TIME_DELAY_NOT_EXPIRED = self.RTDNE = 0x37
        self.UPLOAD_DOWNLOAD_NOT_ACCEPTED = self.UDNA = 0x70
        self.TRANSFER_DATA_SUSPENDED = self.TDS = 0x71
        self.GENERAL_PROGRAMMING_FAILURE = self.GPF = 0x72
        self.WRONG_BLOCK_SEQUENCE_COUNTER = self.WBSC = 0x73
        self.REQUEST_CORRECTLY_RECEIVED_RESPONSE_PENDING = self.RCRRP = 0x78
        self.SUB_FUNCTION_NOT_SUPPORTED_IN_ACTIVE_SESSION = self.SFNSIAS = 0x7E
        self.SERVICE_NOT_SUPPORTED_IN_ACTIVE_SESSION = self.SNSIAS = 0x7F
        self.RPM_TOO_HIGH = self.RPMTH = 0x81
        self.RPM_TOO_LOW = self.RPMTL = 0x82
        self.ENGINE_IS_RUNNING = self.EIR = 0x83
        self.ENGINE_IS_NOT_RUNNING = self.EINR = 0x84
        self.ENGINE_RUN_TIME_TOO_LOW = self.ERTTL = 0x85
        self.TEMPERATURE_TOO_HIGH = self.TEMPTH = 0x86
        self.TEMPERATURE_TOO_LOW = self.TEMPTL = 0x87
        self.VEHICLE_SPEED_TOO_HIGH = self.VSTH = 0x88
        self.VEHICLE_SPEED_TOO_LOW = self.VSTL = 0x89
        self.THROTTLE_OR_PEDAL_TOO_HIGH = self.TPTH = 0x8A
        self.THROTTLE_OR_PEDAL_TOO_LOW = self.TPTL = 0x8B
        self.TRANSMISSION_RANGE_NOT_IN_NEUTRAL = self.TRNIN = 0x8C
        self.TRANSMISSION_RANGE_NOT_IN_GEAR = self.TRNIG = 0x8D
        self.BRAKE_SWITCH_NOT_CLOSED = self.BSNC = 0x8F
        self.SHIFTER_LEVER_NOT_IN_PARK = self.SLNIP = 0x90
        self.TORQUE_CONVERTER_CLUTCH_LOCKED = self.TCCL = 0x91
        self.VOLTAGE_TOO_HIGH = self.VTH = 0x92
        self.VOLTAGE_TOO_LOW = self.VTL = 0x93


class Did:
    """Diagnostic Identifiers (DIDs) for UDS.

    This class contains constants for various diagnostic identifiers.
    """
    def __init__(self) -> None:
        self.VEHICLE_IDENTIFICATION_NUMBER = 0xF190
        self.MANUFACTURER_SPARE_PART_NUMBER = 0xF187
        self.MANUFACTURER_ECU_SOFTWARE_NUMBER = 0xF188
        self.MANUFACTURER_ECU_SOFTWARE_VERSION = 0xF189
        self.ECU_MANUFACTURING_DATE = 0xF18B
        self.ECU_SERIAL_NUMBER = 0xF18C
        self.SUPPORTED_FUNCTIONAL_UNITS = 0xF18D
        self.SYSTEM_SUPPLIER_ECU_SOFTWARE_NUMBER = 0xF194
        self.SYSTEM_SUPPLIER_ECU_SOFTWARE_VERSION = 0xF195
        self.PROGRAMMING_DATE = 0xF199
        self.REPAIR_SHOP_CODE = 0xF198
        self.EXHAUST_REGULATION_TYPE_APPROVAL_NUMBER = 0xF196
        self.INSTALLATION_DATE = 0xF19D
        self.ACTIVE_DIAGNOSTIC_SESSION = 0xFF01


class Memory:
    """A simulated memory map for the UDS server.

    This class holds memory addresses, their corresponding values, and other
    data like DTCs and writable DIDs.

    Attributes:
        writable_dids (list): A list of DIDs that are writable.
        did_data (dict): A dictionary to store data for DIDs.
        memory_map (dict): A dictionary representing the memory layout.
        dtcs (list): A list of Diagnostic Trouble Codes.
    """
    def __init__(self) -> None:
        self.writable_dids = [0xF198, 0xF199]  # Example: Repair Shop Code and Programming Date
        self.did_data = {}
        self.memory_map = {
            0x1000: [0x11, 0x22, 0x33, 0x44],
            0x2000: [0xAA, 0xBB, 0xCC, 0xDD],
        }
        self.dtcs = [
            [0x9A, 0x01, 0x01], # Example DTC 1
            [0x9A, 0x02, 0x01], # Example DTC 2
        ]

    @property
    def vehicle_identification_number(self):
        """The vehicle identification number (VIN)."""
        return split_integer_to_bytes(0x1234567890)

    @property
    def manufacturer_spare_part_number(self):
        """The manufacturer's spare part number."""
        return split_integer_to_bytes(0x1111111111)

    @property
    def manufacturer_ecu_software_number(self):
        """The manufacturer's ECU software number."""
        return split_integer_to_bytes(0x20250801)

    @property
    def manufacturer_ecu_software_version(self):
        """The manufacturer's ECU software version."""
        return split_integer_to_bytes(0x202508010203)

    @property
    def ecu_manufacturing_date(self):
        """The ECU manufacturing date."""
        return split_integer_to_bytes(0x20250801)

    @property
    def ecu_serial_number(self):
        """The ECU serial number."""
        return split_integer_to_bytes(0x1234567890)

    @property
    def supported_functional_units(self):
        """The supported functional units."""
        return split_integer_to_bytes(0x00000001)

    @property
    def system_supplier_ecu_software_number(self):
        """The system supplier's ECU software number."""
        return split_integer_to_bytes(0x20250801)

    @property
    def system_supplier_ecu_software_version(self):
        """The system supplier's ECU software version."""
        return split_integer_to_bytes(0x202508010203)

    @property
    def programming_date(self):
        """The programming date."""
        return split_integer_to_bytes(0x20250801)

    @property
    def repair_shop_code(self):
        """The repair shop code."""
        return split_integer_to_bytes(0x123456)

    @property
    def exhaust_regulation_type_approval_number(self):
        """The exhaust regulation type approval number."""
        return split_integer_to_bytes(0x123456)

    @property
    def ecu_installation_date(self):
        """The ECU installation date."""
        return split_integer_to_bytes(0x20250801)
