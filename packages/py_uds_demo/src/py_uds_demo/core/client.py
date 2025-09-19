from typing import Union
from py_uds_demo.core.server import UdsServer


class UdsClient:
    """A client for sending UDS requests and formatting responses.

    This class interfaces with the UdsServer to send diagnostic requests
    and process the corresponding responses.

    Attributes:
        server (UdsServer): An instance of the UdsServer to process requests.
    """
    def __init__(self) -> None:
        """Initializes the UdsClient.

        This creates a new instance of the UdsServer, which will be used
        for processing all UDS requests initiated by this client.
        """
        self.server = UdsServer()

    def format_request(self, request: list) -> str:
        """Formats a UDS request list into a human-readable string.

        Args:
            request: A list of integers representing the request bytes.

        Returns:
            A string representation of the UDS request, with each byte
            formatted as a two-digit hexadecimal number.
        """
        return "💉 " + " ".join(f"{byte:02X}" for byte in request)

    def _format_response(self, response: list) -> str:
        """Formats a server response list into a human-readable string.

        The formatted string includes a status indicator:
        - 🟢 for a positive response.
        - 🔴 for a negative response.

        Args:
            response: A list of integers representing the response bytes
                from the server.

        Returns:
            A formatted string representation of the server response.
        """
        if response and response[0] == self.server.SID.NEGATIVE_RESPONSE:
            return "🔴 " + " ".join(f"{byte:02X}" for byte in response)
        else:
            return "🟢 " + " ".join(f"{byte:02X}" for byte in response)

    def send_request(
        self, data_stream: Union[list, list[int]], return_formatted_stream: bool
    ) -> Union[list, str]:
        """Sends a UDS request to the server and retrieves the response.

        The request is logged, processed by the server, and the response is
        also logged. The response can be returned as either a raw list of
        bytes or a formatted string.

        Args:
            data_stream: The request data to send to the server, as a list
                of integers.
            return_formatted_stream: If True, the response is returned as a
                formatted string. Otherwise, it is returned as a list of
                integers.

        Returns:
            The server's response, which can be either a list of bytes or a
            formatted string, depending on the value of `return_formatted_stream`.
        """
        self.server.logger.info(self.format_request(data_stream))
        response = self.server.process_request(data_stream)
        formatted_response = self._format_response(response)
        self.server.logger.info(formatted_response)
        if return_formatted_stream:
            return formatted_response
        else:
            return response
