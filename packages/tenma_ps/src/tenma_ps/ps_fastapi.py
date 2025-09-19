import socket
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from tenma_ps.power_supply import TenmaPs

app = FastAPI(
    title="Tenma Power Supply API",
    description=(
        "API for controlling and monitoring a Tenma power supply via the [`TenmaPs`](power_supply.py) class. "
        "See `/docs` for interactive documentation."
    ),
    version="1.0.0"
)

# Singleton device instance (for demo/simple use)
device: Optional[TenmaPs] = None

# ------------------- Pydantic Models -------------------

class ConnectRequest(BaseModel):
    """Request model for connecting to a COM port."""
    port: str

class SetChannelValueRequest(BaseModel):
    """Request model for setting a single value (voltage or current) on a channel."""
    channel: int
    value: float

class SetVoltageCurrentRequest(BaseModel):
    """Request model for setting both voltage and current on a channel."""
    channel: int
    voltage: float
    current: float

# ------------------- API Endpoints -------------------

@app.get("/", tags=["Info"])
def root():
    """
    Root endpoint.

    Returns links to API documentation.
    """
    return {
        "message": "Welcome to Tenma Power Supply API.",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.post("/connect", tags=["Connection"])
def connect(req: ConnectRequest):
    """
    Connect to the Tenma power supply on the specified COM port.

    - **port**: Serial port name (e.g., "COM4")
    """
    global device
    try:
        device = TenmaPs(req.port)
        return {"status": "connected", "port": req.port}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect: {e}")

@app.post("/disconnect", tags=["Connection"])
def disconnect():
    """
    Disconnect from the Tenma power supply.
    """
    global device
    if device is not None:
        try:
            device.close()
            device = None
            return {"status": "disconnected"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to disconnect: {e}")
    else:
        raise HTTPException(status_code=400, detail="No device connected.")

@app.get("/version", tags=["Device Info"])
def get_version():
    """
    Get the version information of the connected Tenma power supply.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    return {"version": device.get_version()}

@app.get("/status", tags=["Device Info"])
def get_status():
    """
    Get the current status of the connected Tenma power supply.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    return {"status": device.get_status()}

@app.post("/turn_on", tags=["Output Control"])
def turn_on():
    """
    Turn ON the power supply output.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    device.turn_on()
    return {"output": "on"}

@app.post("/turn_off", tags=["Output Control"])
def turn_off():
    """
    Turn OFF the power supply output.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    device.turn_off()
    return {"output": "off"}

@app.get("/read_voltage", tags=["Read"])
def read_voltage(channel: int = Query(..., description="Channel number")):
    """
    Read the voltage from a specified channel.

    - **channel**: Channel number to read voltage from.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    voltage = device.read_voltage(channel)
    return {"channel": channel, "voltage": voltage}

@app.get("/read_current", tags=["Read"])
def read_current(channel: int = Query(..., description="Channel number")):
    """
    Read the current from a specified channel.

    - **channel**: Channel number to read current from.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    current = device.read_current(channel)
    return {"channel": channel, "current": current}

@app.post("/set_voltage", tags=["Set"])
def set_voltage(req: SetChannelValueRequest):
    """
    Set the voltage for a specified channel.

    - **channel**: Channel number to set voltage on.
    - **value**: Voltage value in volts.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    device.set_voltage(req.channel, req.value)
    return {"channel": req.channel, "voltage": req.value}

@app.post("/set_current", tags=["Set"])
def set_current(req: SetChannelValueRequest):
    """
    Set the current for a specified channel.

    - **channel**: Channel number to set current on.
    - **value**: Current value in amps.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    device.set_current(req.channel, req.value)
    return {"channel": req.channel, "current": req.value}

@app.post("/set_voltage_current", tags=["Set"])
def set_voltage_current(req: SetVoltageCurrentRequest):
    """
    Set both voltage and current for a specified channel.

    - **channel**: Channel number to set.
    - **voltage**: Voltage value in volts.
    - **current**: Current value in amps.
    """
    if device is None:
        raise HTTPException(status_code=400, detail="No device connected.")
    device.set_voltage(req.channel, req.voltage)
    device.set_current(req.channel, req.current)
    return {"channel": req.channel, "voltage": req.voltage, "current": req.current}

# ------------------- Example Usage -------------------
"""
Example usage with HTTPie or curl:

1. Connect to device:
    http POST http://localhost:8000/connect port="COM4"

2. Get device version:
    http GET http://localhost:8000/version

3. Set voltage and current on channel 1:
    http POST http://localhost:8000/set_voltage_current channel=1 voltage=5.0 current=1.0

4. Read voltage:
    http GET http://localhost:8000/read_voltage channel==1

5. Turn ON output:
    http POST http://localhost:8000/turn_on

6. Disconnect:
    http POST http://localhost:8000/disconnect

Interactive API docs: http://localhost:8000/docs
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("tenma_ps.ps_fastapi:app", host=socket.getfqdn(), reload=True)