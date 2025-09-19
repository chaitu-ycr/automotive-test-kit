import threading
import time
import queue
import customtkinter as ctk
from tkinter import StringVar, IntVar
import serial.tools.list_ports
import sys
import signal

from tenma_ps.power_supply import TenmaPs

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class PsGui(ctk.CTk):
    """
    GUI for controlling and monitoring a Tenma power supply.

    Features:
        - Serial port selection and connection management
        - Read device version
        - Turn power supply ON/OFF
        - Set voltage and current for a specific channel
        - Live display of voltage and current for a selected channel
    """

    def __init__(self):
        """Initialize the GUI and set up all widgets and background threads."""
        super().__init__()
        self.title("Tenma Power Supply GUI")
        self.geometry("540x410")
        self.resizable(False, False)

        # Device state
        self.device: TenmaPs | None = None
        self.is_connected = False
        self.is_monitoring = False

        # Tkinter variables for UI state
        self.selected_port = StringVar()
        self.read_channel_var = IntVar(value=1)
        self.live_voltage_var = StringVar(value="Voltage: -- V")
        self.live_current_var = StringVar(value="Current: -- A")
        self.device_version_var = StringVar(value="Version: --")

        # For set voltage/current section
        self.set_channel_var = IntVar(value=1)
        self.set_voltage_var = StringVar(value="12.50")
        self.set_current_var = StringVar(value="5.00")

        # UI style
        self._button_font = ctk.CTkFont(weight="bold", size=14)
        self._button_text_color = "#ffffff"

        # Threading/worker
        self._action_queue = queue.Queue()
        self._worker_thread = threading.Thread(target=self._process_action_queue, daemon=True)
        self._worker_thread.start()
        self._monitor_thread = None

        self._build_gui()

        # Ensure power supply is closed on exit/signals
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        signal.signal(signal.SIGINT, self._on_signal_exit)
        signal.signal(signal.SIGTERM, self._on_signal_exit)

    # ---------------- GUI Layout ----------------

    def _build_gui(self):
        """Build and layout all GUI sections and widgets."""

        # --- Serial Port Selection (all items in one row) ---
        section_serial = ctk.CTkFrame(self, border_color="#1abc9c", border_width=2)
        section_serial.pack(padx=15, pady=(15, 10), fill="x")

        row_serial = ctk.CTkFrame(section_serial, fg_color="transparent")
        row_serial.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(row_serial, text="Serial Port Selection:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        self.combobox_ports = ctk.CTkComboBox(
            row_serial, values=self._get_available_com_ports(), variable=self.selected_port, width=180
        )
        self.combobox_ports.pack(side="left", padx=(0, 10))
        self.button_connect = ctk.CTkButton(
            row_serial,
            text="Connect",
            command=lambda: self._enqueue_action(self._toggle_connection),
            fg_color="#e74c3c",
            font=self._button_font,
            text_color=self._button_text_color,
            hover_color="#ff7675"
        )
        self.button_connect.pack(side="left")

        # --- Device Version section ---
        section_version = ctk.CTkFrame(self, border_color="#2980b9", border_width=2)
        section_version.pack(padx=15, pady=10, fill="x")
        self.button_version = ctk.CTkButton(
            section_version,
            text="Read Version",
            command=lambda: self._enqueue_action(self._read_device_version),
            state="disabled",
            font=self._button_font,
            text_color=self._button_text_color,
            fg_color="#2980b9",
            hover_color="#74b9ff"
        )
        self.button_version.pack(padx=10, pady=10, side="left")
        self.label_version = ctk.CTkLabel(
            section_version, textvariable=self.device_version_var, font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_version.pack(padx=10, pady=10, side="left")

        # --- Power Control section (Turn ON/OFF) ---
        section_power = ctk.CTkFrame(self, border_color="#9b59b6", border_width=2)
        section_power.pack(padx=15, pady=10, fill="x")

        power_row = ctk.CTkFrame(section_power, fg_color="transparent")
        power_row.pack(padx=10, pady=10, fill="x")

        self.button_on = ctk.CTkButton(
            power_row,
            text="Turn ON",
            command=lambda: self._enqueue_action(self._turn_output_on),
            state="disabled",
            fg_color="#27ae60",
            font=self._button_font,
            text_color=self._button_text_color,
            hover_color="#00ff99",
            width=200,
            height=36
        )
        self.button_on.pack(side="left", padx=(0, 20), fill="x", expand=True)
        self.button_off = ctk.CTkButton(
            power_row,
            text="Turn OFF",
            command=lambda: self._enqueue_action(self._turn_output_off),
            state="disabled",
            fg_color="#c0392b",
            font=self._button_font,
            text_color=self._button_text_color,
            hover_color="#ff7675",
            width=200,
            height=36
        )
        self.button_off.pack(side="left", padx=(0, 0), fill="x", expand=True)

        # --- Set Voltage/Current for Channel section ---
        section_set = ctk.CTkFrame(self, border_color="#e67e22", border_width=2)
        section_set.pack(padx=15, pady=10, fill="x")

        set_row = ctk.CTkFrame(section_set, fg_color="transparent")
        set_row.pack(padx=10, pady=15, fill="x")

        ctk.CTkLabel(set_row, text="Channel:", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.set_channel_entry = ctk.CTkEntry(
            set_row, textvariable=self.set_channel_var, width=40, font=ctk.CTkFont(weight="bold"), state="disabled"
        )
        self.set_channel_entry.pack(side="left", padx=(5, 15))

        ctk.CTkLabel(set_row, text="Voltage (V):", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.set_voltage_entry = ctk.CTkEntry(
            set_row, textvariable=self.set_voltage_var, width=60, font=ctk.CTkFont(weight="bold"), state="disabled"
        )
        self.set_voltage_entry.pack(side="left", padx=(5, 15))

        ctk.CTkLabel(set_row, text="Current (A):", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.set_current_entry = ctk.CTkEntry(
            set_row, textvariable=self.set_current_var, width=60, font=ctk.CTkFont(weight="bold"), state="disabled"
        )
        self.set_current_entry.pack(side="left", padx=(5, 15))

        self.button_set = ctk.CTkButton(
            set_row,
            text="Set",
            command=lambda: self._enqueue_action(self._set_channel_voltage_current),
            state="disabled",
            fg_color="#16a085",
            font=self._button_font,
            text_color=self._button_text_color,
            hover_color="#1abc9c"
        )
        self.button_set.pack(side="left", padx=(10, 0))

        # --- Live Voltage/Current Reading section ---
        section_read = ctk.CTkFrame(self, border_color="#34495e", border_width=2)
        section_read.pack(padx=15, pady=10, fill="x")

        row_read = ctk.CTkFrame(section_read, fg_color="transparent")
        row_read.pack(padx=10, pady=15, fill="x")

        ctk.CTkLabel(row_read, text="Channel:", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.read_channel_entry = ctk.CTkEntry(
            row_read, textvariable=self.read_channel_var, width=40, font=ctk.CTkFont(weight="bold")
        )
        self.read_channel_entry.pack(side="left", padx=(5, 20))

        self.label_voltage = ctk.CTkLabel(
            row_read, textvariable=self.live_voltage_var, font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_voltage.pack(side="left", padx=(0, 20))
        self.label_current = ctk.CTkLabel(
            row_read, textvariable=self.live_current_var, font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_current.pack(side="left")

    # ---------------- Serial Port Helpers ----------------

    def _get_available_com_ports(self):
        """Return a list of available COM port device names."""
        return [p.device for p in serial.tools.list_ports.comports()]

    # ---------------- Action Queue/Worker ----------------

    def _enqueue_action(self, func):
        """Add a function to the action queue to be executed in the worker thread."""
        self._action_queue.put(func)

    def _process_action_queue(self):
        """Continuously process actions from the queue in a background thread."""
        while True:
            func = self._action_queue.get()
            try:
                func()
            except Exception as e:
                self._show_error_mainthread(f"Error: {e}")
            self._action_queue.task_done()

    # ---------------- Device Actions ----------------

    def _toggle_connection(self):
        """Connect or disconnect from the power supply based on current state."""
        if not self.is_connected:
            port = self.selected_port.get()
            if not port:
                self._show_error_mainthread("Please select a COM port.")
                return
            try:
                self.device = TenmaPs(port)
                self.is_connected = True
                self._after_mainthread(self._on_connect_success)
            except Exception as e:
                self._show_error_mainthread(f"Failed to connect: {e}")
        else:
            self._disconnect_device()

    def _on_connect_success(self):
        """Update UI after successful connection."""
        self.button_connect.configure(text="Disconnect", fg_color="#27ae60")
        self.combobox_ports.configure(state="disabled")
        self.button_on.configure(state="normal")
        self.button_off.configure(state="normal")
        self.button_version.configure(state="normal")
        self.button_set.configure(state="normal")
        self.set_channel_entry.configure(state="normal")
        self.set_voltage_entry.configure(state="normal")
        self.set_current_entry.configure(state="normal")
        self._start_monitoring()

    def _disconnect_device(self):
        """Disconnect from the power supply and reset UI."""
        self._stop_monitoring()
        if self.device:
            try:
                self.device.close()
            except Exception:
                pass
        self.device = None
        self.is_connected = False
        self.button_connect.configure(text="Connect", fg_color="#e74c3c")
        self.combobox_ports.configure(state="normal")
        self.button_on.configure(state="disabled")
        self.button_off.configure(state="disabled")
        self.button_version.configure(state="disabled")
        self.button_set.configure(state="disabled")
        self.set_channel_entry.configure(state="disabled")
        self.set_voltage_entry.configure(state="disabled")
        self.set_current_entry.configure(state="disabled")
        self.live_voltage_var.set("Voltage: -- V")
        self.live_current_var.set("Current: -- A")
        self.device_version_var.set("Version: --")

    def _start_monitoring(self):
        """Start background thread to monitor live voltage and current."""
        self.is_monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_live_values, daemon=True)
        self._monitor_thread.start()

    def _stop_monitoring(self):
        """Stop the background monitoring thread."""
        self.is_monitoring = False
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1)

    def _monitor_live_values(self):
        """Continuously read voltage and current from the selected channel and update the UI."""
        while self.is_monitoring and self.device:
            try:
                channel = self.read_channel_var.get()
                voltage = self.device.read_voltage(channel=channel)
                current = self.device.read_current(channel=channel)
                self._after_mainthread(lambda: self.live_voltage_var.set(f"Voltage: {voltage:.2f} V"))
                self._after_mainthread(lambda: self.live_current_var.set(f"Current: {current:.2f} A"))
            except Exception:
                self._after_mainthread(lambda: self.live_voltage_var.set("Voltage: -- V"))
                self._after_mainthread(lambda: self.live_current_var.set("Current: -- A"))
            time.sleep(1)

    def _turn_output_on(self):
        """Turn ON the power supply output."""
        if self.device:
            try:
                self.device.turn_on()
                self._after_mainthread(lambda: self.button_on.configure(state="disabled"))
                self._after_mainthread(lambda: self.button_off.configure(state="normal"))
            except Exception as e:
                self._show_error_mainthread(f"Failed to turn ON: {e}")

    def _turn_output_off(self):
        """Turn OFF the power supply output."""
        if self.device:
            try:
                self.device.turn_off()
                self._after_mainthread(lambda: self.button_on.configure(state="normal"))
                self._after_mainthread(lambda: self.button_off.configure(state="disabled"))
            except Exception as e:
                self._show_error_mainthread(f"Failed to turn OFF: {e}")

    def _read_device_version(self):
        """Read and display the device version."""
        if self.device:
            try:
                version = self.device.get_version()
                self._after_mainthread(lambda: self.device_version_var.set(f"Version: {version}"))
            except Exception as e:
                self._after_mainthread(lambda: self.device_version_var.set("Version: --"))
                self._show_error_mainthread(f"Failed to read version: {e}")

    def _set_channel_voltage_current(self):
        """Set voltage and current for the specified channel using the set section."""
        if self.device:
            try:
                channel = self.set_channel_var.get()
                voltage_input = self.set_voltage_var.get()
                current_input = self.set_current_var.get()

                # Validate voltage and current inputs
                try:
                    voltage = float(voltage_input)
                except ValueError:
                    raise ValueError(f"Invalid voltage input: '{voltage_input}'")

                try:
                    current = float(current_input)
                except ValueError:
                    raise ValueError(f"Invalid current input: '{current_input}'")

                self.device.set_voltage(channel=channel, voltage=voltage)
                self.device.set_current(channel=channel, current=current)
            except Exception as e:
                self._show_error_mainthread(f"Failed to set voltage/current: {e}")

    # ---------------- Thread-safe GUI update helpers ----------------

    def _after_mainthread(self, func):
        """Schedule a function to run on the main thread."""
        self.after(0, func)

    def _show_error_mainthread(self, message):
        """Show an error message in a thread-safe way."""
        self._after_mainthread(lambda: self._show_error_popup(message))

    def _show_error_popup(self, message):
        """Display an error message in a popup window."""
        error_win = ctk.CTkToplevel(self)
        error_win.title("Error")
        error_win.geometry("300x100")
        ctk.CTkLabel(error_win, text=message, text_color="red", font=ctk.CTkFont(weight="bold", size=13)).pack(padx=20, pady=20)
        ctk.CTkButton(error_win, text="OK", command=error_win.destroy, font=self._button_font, text_color=self._button_text_color).pack(pady=(0, 10))

    # ---------------- Cleanup/Exit ----------------

    def _on_close(self):
        """Handle GUI close event and ensure power supply is closed."""
        self._stop_monitoring()
        if self.device:
            try:
                self.device.close()
            except Exception:
                pass
        self.destroy()

    def _on_signal_exit(self, signum, frame):
        """Handle process signals to ensure power supply is closed."""
        self._on_close()
        sys.exit(0)


if __name__ == "__main__":
    app = PsGui()
    app.mainloop()