from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from py_uds_demo.core.client import UdsClient

app = FastAPI()
client = UdsClient()

class UdsRequest(BaseModel):
    data: List[int]

@app.post("/send_request")
async def send_request(request: UdsRequest):
    """
    Sends a UDS request to the server.
    """
    response = client.send_request(request.data, False)
    return {"response": response}

@app.get("/help/{sid}")
async def get_help(sid: int):
    """
    Returns the docstring for a given service ID.
    """
    service = client.server.service_map.get(sid)
    if service:
        return {"docstring": service.__doc__}
    else:
        raise HTTPException(status_code=404, detail=f"No help found for SID 0x{sid:02X}")
