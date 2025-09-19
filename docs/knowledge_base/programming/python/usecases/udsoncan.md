# 🚗 Usecase: Vehicle Diagnostics with `udsoncan`

**UDS (Unified Diagnostic Services)** is the standard protocol (ISO 14229-1) used in the automotive industry to diagnose, test, and configure electronic control units (ECUs). It allows you to ask an ECU questions like "What's your serial number?" (Read Data by Identifier) or give it commands like "Reset yourself" (ECU Reset).

These UDS messages are typically sent over a CAN bus using a transport protocol called **ISO-TP** (ISO 15765-2). The `udsoncan` library is a powerful Python tool that handles all the complexity of the UDS and ISO-TP layers, allowing you to interact with ECUs using a clean, high-level API.

## 🗺️ A Mind Map of the UDS Stack

`udsoncan` sits on top of other libraries to provide a full diagnostic stack.

```mermaid
graph TD
    A[Your Python Script] --> B{udsoncan Client};
    B --> C(UDS Services e.g., ReadDataByIdentifier);
    C --> D{ISO-TP Connection};
    D --> E{python-can Bus};
    E --> F[CAN Hardware];
    F --> G[ECU];

    style B fill:#bbf,stroke:#333,stroke-width:2px
```

---

## 🤔 What Is `udsoncan`?

`udsoncan` is a Python implementation of the UDS protocol. It allows you to write scripts that act as a diagnostic "client" (like a mechanic's scan tool) to communicate with an ECU "server." It abstracts away the byte-level details of constructing service requests and parsing responses.

## ✨ Why Is `udsoncan` So Useful?

*   **It Implements the Standard:** It provides a comprehensive implementation of the UDS services, saving you from having to read the entire ISO standard and implement it from scratch.
*   **Simplifies Complex Operations:** Tasks like unlocking a security-protected ECU, which involve a multi-step seed-and-key exchange, are handled by the library.
*   **Built for Automation:** It's designed for writing automated diagnostic test scripts, which are essential for validating ECU software.
*   **Works with `python-can`:** It integrates directly with the `python-can` library, allowing you to use it with a wide variety of CAN hardware interfaces.

---

## 🚀 How Do I Use `udsoncan`?

Let's walk through a typical diagnostic session workflow.

### 1. Installation

You'll need `udsoncan` and a transport layer library like `python-can-isotp`.
```bash
pip install udsoncan python-can python-can-isotp
```

### 2. Setting Up the Connection

First, you need to establish the communication stack. This involves creating a `python-can` bus object and then wrapping it in an ISO-TP connection object.

```python
import can
import isotp
from udsoncan.connections import PythonIsoTpConnection

# 1. Create the python-can bus object (hardware interface)
# Replace with your actual hardware interface
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)

# 2. Define the ISO-TP addresses for the client and ECU
# The client sends to the ECU's request ID (e.g., 0x7E0)
# and listens on the ECU's response ID (e.g., 0x7E8)
tp_address = isotp.Address(
    addressing_mode=isotp.AddressingMode.Normal_11bits,
    txid=0x7E0, # ECU Request ID
    rxid=0x7E8  # ECU Response ID
)

# 3. Create the ISO-TP connection
# This handles breaking down long messages into multiple CAN frames
stack = isotp.CanStack(bus=bus, address=tp_address)
conn = PythonIsoTpConnection(stack)
```

### 3. Using the UDS Client

The `Client` object is your main tool for interacting with the ECU. The `with` statement is recommended as it ensures the connection is properly closed.

Let's perform a common sequence: change session, unlock security, and read a protected data identifier.

```python
from udsoncan.client import Client
from udsoncan.services import * # Import all UDS services
import time

# The client needs the connection object and a config dictionary
# The config tells the client how to handle certain services, like security access
client_config = {
  'security_algo': lambda level, seed: bytes([s+1 for s in seed]), # Dummy security algorithm
  'exception_on_negative_response': True,
  'request_timeout': 5,
}

with Client(conn, config=client_config) as client:
  try:
    # 1. Change to a session that allows more services
    client.change_session(DiagnosticSessionControl.ExtendedDiagnosticSession)
    print("Switched to Extended Diagnostic Session.")
    time.sleep(0.1)

    # 2. Unlock a security level
    # This will automatically perform the seed-and-key exchange
    # using the 'security_algo' function defined in our config.
    client.unlock_security_access(SecurityAccess.Level1)
    print("Security Level 1 unlocked.")
    time.sleep(0.1)

    # 3. Now we can access protected services
    # For example, read the Vehicle Identification Number (VIN)
    response = client.read_data_by_identifier(DataIdentifier.VehicleIdentificationNumber)
    vin = response.service_data.values[DataIdentifier.VehicleIdentificationNumber]
    print(f"Successfully read VIN: {vin}")

  except udsoncan.exceptions.NegativeResponseException as e:
    print(f"ECU returned a negative response: {e.response}")
  except udsoncan.exceptions.InvalidResponseException as e:
    print(f"ECU returned an invalid response: {e}")
  finally:
    # 4. Always return to the default session when done
    client.ecu_reset(ECUReset.HardReset)
    print("ECU reset to default state.")
```
This example shows how `udsoncan` simplifies a complex, multi-step diagnostic procedure into a clean, readable Python script.
