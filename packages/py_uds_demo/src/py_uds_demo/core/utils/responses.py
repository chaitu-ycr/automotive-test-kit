class PositiveResponse:
    """Handles the creation of positive UDS responses."""

    def __init__(self) -> None:
        """Initializes the PositiveResponse handler."""
        pass

    def report_positive_response(self, sid: int, data: list) -> list:
        """Constructs a positive response message.

        Args:
            sid: The service identifier of the request.
            data: A list of integers representing the response data.

        Returns:
            A list of integers representing the complete positive response
            message, including the positive response SID.
        """
        return [sid + 0x40] + data


class NegativeResponse:
    """Handles the creation of negative UDS responses."""

    def __init__(self) -> None:
        """Initializes the NegativeResponse handler."""
        pass

    def report_negative_response(self, sid: int, nrc: int) -> list:
        """Constructs a negative response message.

        Args:
            sid: The service identifier of the request.
            nrc: The negative response code.

        Returns:
            A list of integers representing the complete negative response
            message.
        """
        return [0x7F, sid, nrc]

    def check_subfunction_supported(
        self, sfid: int, supported_subfunctions: list
    ) -> bool:
        """Checks if a sub-function is supported.

        Args:
            sfid: The sub-function identifier to check.
            supported_subfunctions: A list of supported sub-function
                identifiers.

        Returns:
            True if the sub-function is supported, False otherwise.
        """
        return sfid in supported_subfunctions
