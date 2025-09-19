# 🛶 Usecase: Automating CANoe with `py_canoe`

**Vector CANoe** is the industry-standard tool for developing, testing, and analyzing automotive electronic control units (ECUs) and networks. While it's incredibly powerful for manual testing and simulation, its true power in a modern workflow is unleashed through **automation**.

`py_canoe` is a Python package that acts as a bridge, allowing you to control and interact with the CANoe application directly from your Python scripts. This enables you to build powerful, automated test sequences, manipulate signals, run diagnostics, and generate reports, all using the flexibility of Python.

## 🗺️ A Mind Map of `py_canoe`'s Capabilities

`py_canoe` provides programmatic access to almost all of CANoe's core features.

```mermaid
mindmap
  root((`py_canoe`))
    --> Measurement Control
      --> `.open()`, `.start_measurement()`, `.stop_measurement()`
      --> `.quit()`
    --> Bus Interaction
      --> Get/Set Signals: `.get_signal_value()`, `.set_signal_value()`
      --> Bus Statistics: `.get_can_bus_statistics()`
      --> Diagnostics: `.send_diag_request()`
    --> Variable Access
      --> System Variables: `sys_var`
      --> Environment Variables: `env_var`
    --> Test Automation
      --> CAPL: `.call_capl_function()`
      --> Test Modules: `.execute_test_module()`
    --> Logging & Reporting
      --> Write Window: `.write_text_in_write_window()`
      --> Logging Blocks
```

---

## 🤔 What Is `py_canoe`?

`py_canoe` is a Python wrapper around the CANoe COM API. The COM API is an interface provided by Vector that allows external applications to control CANoe. `py_canoe` simplifies this interface, making it easy and "Pythonic" to write automation scripts.

## ✨ Why Is `py_canoe` So Useful?

*   **Automate Repetitive Testing:** Manually running the same test sequences over and over is time-consuming and prone to error. With `py_canoe`, you can write a script to do it perfectly every time.
*   **Integrate with Python's Ecosystem:** You can use other powerful Python libraries like `pandas` for data analysis, `matplotlib` for plotting results, or `pytest` for structuring your tests, all while controlling CANoe.
*   **Build Complex Test Scenarios:** Programmatically change signals, check system variables, and send diagnostic requests in ways that would be difficult or impossible to do manually.
*   **Continuous Integration (CI/CD):** `py_canoe` scripts can be integrated into CI/CD pipelines (like Jenkins) to automatically run regression tests on your ECUs whenever new code is committed.

---

## 🚀 How Do I Automate CANoe?

Let's walk through a typical automated test scenario.

### 1. Installation

First, you need to install the library.
```bash
pip install py-canoe
```

### 2. The Basic Workflow: Setup, Execute, Teardown

A typical automation script follows these steps:
1.  **Setup:** Initialize the `CANoe` object, open a configuration file.
2.  **Execute:** Start the measurement, perform your test actions (manipulate signals, call functions, etc.), and check for results.
3.  **Teardown:** Stop the measurement and close CANoe.

```python
from py_canoe import CANoe

def main():
    # 1. Setup
    canoe = CANoe()
    canoe.open(r'C:\path\to\your\demo.cfg')

    # 2. Execute
    canoe.start_measurement()

    # --- Your test logic goes here! ---
    print("Measurement is running...")
    # For example, let's set a signal value.
    canoe.set_signal_value('CAN', 1, 'LightState', 'FlashLight', 1)

    # Wait for a few seconds to observe the change
    import time
    time.sleep(5)

    # 3. Teardown
    canoe.stop_measurement()
    canoe.quit()
    print("Test finished.")

if __name__ == "__main__":
    main()
```

### 3. Interacting with Signals and Variables

This is the core of most test cases. You can read and write to signals, system variables, and environment variables.

**Working with Signals:**
```python
# Set the value of a signal on CAN channel 1
canoe.set_signal_value('CAN', 1, 'LightState', 'FlashLight', 1)

# Get the value of a signal
flash_light_status = canoe.get_signal_value('CAN', 1, 'LightState', 'FlashLight')
print(f"FlashLight status is: {flash_light_status}")
```

**Working with System Variables:**
System variables are a powerful way to communicate between your Python script and your CAPL code.
```python
# Set a system variable in the 'demo' namespace
canoe.set_system_variable_value('demo::sys_var1', 123)

# Get the value back
sys_var_value = canoe.get_system_variable_value('demo::sys_var1')
```

### 4. Running Diagnostics

You can easily send diagnostic requests and receive responses.

```python
# Send a diagnostic request by service name defined in the CDD
response = canoe.send_diag_request('Door', 'DefaultSession_Start')
print(f"Diag Response: {response.response_code}, Data: {response.data}")

# You can also send raw hex requests
raw_response = canoe.send_diag_request('Door', '10 02')
```

### 5. Executing Test Modules

For more structured testing, you can trigger CANoe Test Modules directly from Python.

```python
# Execute all test modules in the environment
canoe.execute_all_test_modules()

# Or execute a specific test module by name
canoe.execute_test_module('MyTestModule')
```
By combining the power of CANoe's simulation environment with the flexibility of Python scripting, `py_canoe` enables robust and scalable automated testing for automotive systems.
