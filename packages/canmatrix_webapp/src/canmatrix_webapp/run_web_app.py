"""
canmatrix_webapp – Streamlit Web Application Launcher

This module provides the command-line entry point for launching the canmatrix Streamlit web application.
It allows users to interact with CAN matrix files through a browser-based UI, supporting file upload,
exploration, and export in various formats.

Features:
    - Command-line interface for specifying server bind address and port.
    - Automatic discovery and launch of the Streamlit app defined in 'web_app.py'.
    - Logging for startup, errors, and process management.

Example usage:
    python -m canmatrix_webapp.run_web_app [--server-address ADDRESS] [--server-port PORT]

Arguments:
    --server-address   Address to bind the Streamlit server (default: system FQDN)
    --server-port      Port to run the Streamlit server on (default: 8502)
"""

import os
import sys
import socket
import subprocess
import logging
from pathlib import Path
from typing import Optional
import argparse

logging.basicConfig(
    level=getattr(logging, os.environ.get("CANMATRIX_WEBAPP_LOGLEVEL", "INFO").upper(), logging.INFO),
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

class WebAppLauncher:
    """
    Command-line interface and process launcher for the canmatrix Streamlit web application.

    Methods:
        launch(address: Optional[str], port: int) -> bool:
            Launches the Streamlit web application at the specified address and port.

        parse_args() -> argparse.Namespace:
            Parses command-line arguments for server address and port.
    """

    @staticmethod
    def launch(address: Optional[str] = None, port: int = 8502) -> bool:
        """
        Launch the canmatrix Streamlit web application.

        Args:
            address (Optional[str]): Address to bind the server. If None, uses system FQDN.
            port (int): Port to run the server on. Defaults to 8502.

        Returns:
            bool: True if the application started successfully, False otherwise.
        """
        app_file = Path(__file__).parent / "web_app.py"
        if not app_file.is_file():
            logger.error("web_app.py not found at %s", app_file)
            return False
        bind_address = address or socket.getfqdn()
        cmd = [
            sys.executable, "-m", "streamlit", "run", str(app_file),
            "--server.address", bind_address,
            "--server.port", str(port)
        ]
        logger.debug("Executing command: %s", ' '.join(cmd))
        try:
            subprocess.Popen(cmd)
            logger.info("Streamlit app started at http://%s:%d", bind_address, port)
            return True
        except Exception as exc:
            logger.exception("Failed to start Streamlit app: %s", exc)
            return False

    @staticmethod
    def parse_args() -> argparse.Namespace:
        """
        Parse command-line arguments for server address and port.

        Returns:
            argparse.Namespace: Parsed arguments with 'server_address' and 'server_port' attributes.
        """
        parser = argparse.ArgumentParser(
            description="Launch the canmatrix Streamlit web application."
        )
        parser.add_argument(
            "--server-address",
            type=str,
            default=None,
            help="Bind address for the Streamlit server (default: system FQDN)"
        )
        parser.add_argument(
            "--server-port",
            type=int,
            default=8502,
            help="Port for the Streamlit server (default: 8502)"
        )
        return parser.parse_args()

def main():
    """
    Main entry point for launching the canmatrix Streamlit web application.
    Parses command-line arguments and starts the web application.
    """
    args = WebAppLauncher.parse_args()
    if not WebAppLauncher.launch(args.server_address, args.server_port):
        sys.exit(1)

if __name__ == '__main__':
    main()