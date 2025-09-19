import socket
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from hid_usb_relay.usb_relay import (
    set_relay_device_state,
    set_relay_device_relay_state,
    get_relay_device_state,
    get_relay_device_relay_state,
    set_default_relay_device_state,
    set_default_relay_device_relay_state,
    get_default_relay_device_state,
    get_default_relay_device_relay_state,
)

app = FastAPI()

logging.basicConfig(level=logging.INFO)

helper_text = """
<h1>YCR HID USB Relay Web API</h1>
<h2>Endpoints</h2>
<ul>
    <li><b>/</b> ➖ This page</li>
    <li><b>/relay/1/on</b> ➖ Turn ON Relay 1 of Default Relay Device</li>
    <li><b>/relay/2/off</b> ➖ Turn OFF Relay 2 of Default Relay Device</li>
    <li><b>/relay/all/on</b> ➖ Turn ON all Relays of Default Relay Device</li>
    <li><b>/relay/all/off</b> ➖ Turn OFF all Relays of Default Relay Device</li>
    <li><b>/relay/HURTM/1/on</b> ➖ Turn ON Relay 1 of Relay Id "HURTM"</li>
    <li><b>/relay/HURTM/2/off</b> ➖ Turn OFF Relay 2 of Relay Id "HURTM"</li>
    <li><b>/relay/HURTM/all/on</b> ➖ Turn ON all Relays of Relay Id "HURTM"</li>
    <li><b>/relay/HURTM/all/off</b> ➖ Turn OFF all Relays of Relay Id "HURTM"</li>
</ul>
"""

@app.get("/", response_class=HTMLResponse)
def root_page_help() -> str:
    """
    Provides help text for the root page.

    Returns:
        str: The help text for the root page.
    """
    return helper_text

@app.get("/relay/{relay_id}/{relay_number}/{relay_state}")
def relay_control_by_id(relay_id: str, relay_number: str, relay_state: str) -> dict:
    """
    Controls the state of a relay by its ID and relay number.

    Args:
        relay_id (str): The ID of the relay device.
        relay_number (str): The number of the relay to control. Use "all" to control all relays.
        relay_state (str): The desired state of the relay (e.g., "on", "off").

    Returns:
        dict: A dictionary containing the status of the operation and the current state of the relay.

    Raises:
        HTTPException: If the relay state could not be set or if an internal server error occurs.
    """
    try:
        if relay_number.lower() == "all":
            ret_val = set_relay_device_state(relay_id, relay_state.upper())
        else:
            ret_val = set_relay_device_relay_state(relay_id, relay_number, relay_state.upper())

        if ret_val:
            if relay_number.lower() == "all":
                response_text = get_relay_device_state(relay_id)
            else:
                response_text = get_relay_device_relay_state(relay_id, relay_number)
            return {"status": "success", "relay_state": response_text}
        else:
            raise HTTPException(status_code=400, detail="Failed to set relay state. Check command.")
    except Exception as e:
        logging.error(f"Error in relay_control_by_id: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/relay/{relay_number}/{relay_state}")
def default_relay_control(relay_number: str, relay_state: str) -> dict:
    """
    Controls the state of a relay or all relays on the default relay device.

    Args:
        relay_number (str): The relay number to control. Use "all" to control all relays.
        relay_state (str): The desired state of the relay(s). Typically "on" or "off".

    Returns:
        dict: A dictionary containing the status of the operation and the current state of the relay(s).

    Raises:
        HTTPException: If the relay state could not be set or if an internal error occurs.
    """
    try:
        if relay_number.lower() == "all":
            ret_val = set_default_relay_device_state(relay_state.upper())
        else:
            ret_val = set_default_relay_device_relay_state(relay_number, relay_state.upper())

        if ret_val:
            if relay_number.lower() == "all":
                response_text = get_default_relay_device_state()
            else:
                response_text = get_default_relay_device_relay_state(relay_number)
            return {"status": "success", "relay_state": response_text}
        else:
            raise HTTPException(status_code=400, detail="Failed to set relay state. Check command.")
    except Exception as e:
        logging.error(f"Error in default_relay_control: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host=socket.getfqdn(), port=9400)
