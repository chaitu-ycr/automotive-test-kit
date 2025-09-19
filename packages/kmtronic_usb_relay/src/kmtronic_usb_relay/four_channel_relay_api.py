import os
import sys
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Path
import uvicorn

from kmtronic_usb_relay.four_channel_relay import RelayController
from kmtronic_usb_relay.com_utils import SerialComUtils

def create_app(com_port: str, controller: Optional[RelayController] = None) -> FastAPI:
    """
    Create and configure a FastAPI app for the KMTronic 4-Channel USB Relay.

    Args:
        com_port: Serial port for the relay board.
        controller: Optional RelayController instance (for testing/mocking).

    Returns:
        Configured FastAPI app.
    """
    relay_controller = controller or RelayController(com_port)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        relay_controller.close()

    app = FastAPI(title="KMTronic USB Relay API", lifespan=lifespan)

    @app.get("/health", response_model=Dict[str, str])
    def health_check() -> Dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok"}

    @app.get("/", response_model=Dict[str, Any])
    def root() -> Dict[str, Any]:
        endpoints = [
            {"path": route.path, "methods": list(route.methods)}
            for route in app.routes
            if hasattr(route, "path") and hasattr(route, "methods")
        ]
        return {
            "message": "KMTronic USB Relay API is running.",
            "endpoints": endpoints
        }

    @app.get("/relay/status", response_model=Dict[str, Any])
    def get_status() -> Dict[str, Any]:
        """Get the status of all relays."""
        return relay_controller.get_statuses()

    @app.post("/relay/{relay_number}/on", response_model=Dict[str, Any])
    def turn_on(
        relay_number: int = Path(..., ge=1, le=4, description="Relay number (1-4)")
    ) -> Dict[str, Any]:
        """Turn ON the specified relay."""
        try:
            relay_controller.turn_on(relay_number)
            return {"result": "Relay turned ON", "relay": relay_number}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/relay/{relay_number}/off", response_model=Dict[str, Any])
    def turn_off(
        relay_number: int = Path(..., ge=1, le=4, description="Relay number (1-4)")
    ) -> Dict[str, Any]:
        """Turn OFF the specified relay."""
        try:
            relay_controller.turn_off(relay_number)
            return {"result": "Relay turned OFF", "relay": relay_number}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return app

def get_app() -> FastAPI:
    """
    Get a FastAPI app instance for ASGI servers (e.g., uvicorn).
    Uses the KMTRONIC_COM_PORT environment variable or defaults to 'COM4'.
    """
    com_port = os.getenv("KMTRONIC_COM_PORT", "COM4")
    return create_app(com_port)

class RelayControllerApi:
    """
    User-friendly wrapper to run the FastAPI server for KMTronic USB Relay.

    Example:
        api = RelayControllerApi("COM4")
        api.run()
    """

    def __init__(self, com_port: str = "COM4", controller: Optional[RelayController] = None):
        """
        Initialize the API server wrapper.

        Args:
            com_port: Serial port for the relay board (e.g., "COM4" or "/dev/ttyUSB0").
            controller: Optional RelayController instance for testing/mocking.
        """
        self.app = create_app(com_port, controller)

    def run(self, host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
        """
        Start the FastAPI server using uvicorn.

        Args:
            host: Hostname or IP address to bind the server.
            port: Port number to bind the server.
            reload: Enable auto-reload (for development).
        """
        uvicorn.run(self.app, host=host, port=port, reload=reload)

def select_com_port() -> Optional[str]:
    """
    Helper to select a COM port interactively if not provided.
    Returns the selected COM port or None if not available.
    """
    ports = SerialComUtils.get_port_names()
    if not ports:
        print("No serial COM ports found. Please connect your relay and try again.")
        return None
    print("Available COM ports:")
    for idx, port in enumerate(ports, 1):
        print(f"  {idx}: {port}")
    while True:
        selection = input(f"Select COM port [1-{len(ports)}]: ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(ports):
            return ports[int(selection) - 1]
        print("Invalid selection. Please try again.")

def main() -> None:
    """
    Command-line entry point to run the API server.

    Usage:
        ``python -m src.kmtronic_usb_relay.four_channel_relay_api [COM_PORT] [--host HOST] [--port PORT] [--reload]``
    """
    import argparse

    parser = argparse.ArgumentParser(description="Run KMTronic USB Relay API server.")
    parser.add_argument(
        "com_port",
        nargs="?",
        default=None,
        help="COM port for relay board (e.g., COM4 or /dev/ttyUSB0)."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (for development)")
    args = parser.parse_args()

    com_port = args.com_port or os.getenv("KMTRONIC_COM_PORT")
    if not com_port:
        com_port = select_com_port()
        if not com_port:
            sys.exit(1)

    api = RelayControllerApi(com_port)
    api.run(host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
