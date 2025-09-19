import logging
import threading
from typing import List, Optional

import customtkinter as ctk
import tkinter.messagebox as messagebox

from kmtronic_usb_relay.com_utils import SerialComUtils
from kmtronic_usb_relay.four_channel_relay import RelayController

class RelayControllerGui:
    """
    User-friendly GUI for KMTronic USB 4-channel relay module.
    Provides an interface to connect, control, and monitor relays.
    """

    def __init__(
        self,
        com_port: str = "",
        controller: Optional[RelayController] = None,
        relay_names: Optional[List[str]] = None,
    ):
        """
        Initialize the RelayControllerGui.

        Args:
            com_port (str): Default COM port to select.
            controller (Optional[RelayController]): Optional pre-initialized RelayController.
            relay_names (Optional[List[str]]): Optional list of relay names for labeling buttons.
        """
        self.controller = controller
        self.com_port = com_port
        self.relay_names = relay_names or [f"Relay {i}" for i in range(1, 5)]
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.root.title("KMTronic USB Relay Controller")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.relay_buttons: List[ctk.CTkButton] = []
        self.combobox = None
        self.conn_btn = None
        self._build_ui()
        self._update_ui()

    def _build_ui(self):
        """
        Build the main UI layout, including port selection, relay controls, and action buttons.
        """
        main = ctk.CTkFrame(self.root, fg_color="#23272e")
        main.pack(padx=1, pady=1, fill="both", expand=True)
        self._build_port_group(main)
        self._build_relay_group(main)
        self._build_action_group(main)

    def _build_port_group(self, parent):
        """
        Build the serial port selection group in the UI.

        Args:
            parent: The parent widget to attach this group to.
        """
        port_group = ctk.CTkFrame(parent, border_color="#1976D2", border_width=2, fg_color="#23272e")
        port_group.pack(fill="x", pady=(0, 4), padx=1, ipady=2, ipadx=2)
        ctk.CTkLabel(
            port_group, text="Port:", width=50, anchor="w", text_color="#B0B8C1",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, padx=(4, 1), pady=4, sticky="w")
        ports = SerialComUtils.get_port_names()
        self.combobox = ctk.CTkComboBox(
            port_group, values=ports, width=120, fg_color="#23272e", border_color="#1976D2"
        )
        self.combobox.grid(row=0, column=1, padx=1, pady=4, sticky="w")
        self.combobox.set(self.com_port if self.com_port in ports else (ports[0] if ports else ""))
        ctk.CTkButton(
            port_group, text="⟳", width=28, command=self.refresh_ports,
            fg_color="#23272e", border_color="#1976D2"
        ).grid(row=0, column=2, padx=1, pady=4)
        self.conn_btn = ctk.CTkButton(
            port_group, text="Connect", fg_color="#444c56", hover_color="#1976D2",
            width=90, command=self._toggle_connection
        )
        self.conn_btn.grid(row=0, column=3, padx=(6, 1), pady=4)
        port_group.grid_columnconfigure(4, weight=1)

    def _build_relay_group(self, parent):
        """
        Build the relay control buttons in the UI.

        Args:
            parent: The parent widget to attach this group to.
        """
        relay_group = ctk.CTkFrame(parent, border_color="#388E3C", border_width=2, fg_color="#23272e")
        relay_group.pack(fill="x", pady=(0, 4), padx=1, ipady=2, ipadx=2)
        ctk.CTkLabel(
            relay_group, text="Relay Controls", font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#A5D6A7"
        ).pack(anchor="w", padx=4, pady=(4, 6))
        row = ctk.CTkFrame(relay_group, fg_color="#23272e")
        row.pack(fill="x", padx=6, pady=(0, 4))
        for i in range(1, 5):
            col = ctk.CTkFrame(row, fg_color="#23272e")
            col.pack(side="left", padx=6, expand=True)
            relay_label = self.relay_names[i - 1] if i - 1 < len(self.relay_names) else f"Relay {i}"
            ctk.CTkLabel(
                col, text=relay_label, width=60, anchor="center", text_color="#B0B8C1",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=(0, 2))
            btn = ctk.CTkButton(
                col, text="OFF", fg_color="#444c56", hover_color="#388E3C", width=70,
                command=lambda n=i: self._toggle_relay(n)
            )
            btn.pack()
            self.relay_buttons.append(btn)

    def _build_action_group(self, parent):
        """
        Build the action buttons group (e.g., Refresh Status) in the UI.

        Args:
            parent: The parent widget to attach this group to.
        """
        btn_frame = ctk.CTkFrame(parent, fg_color="#23272e", border_color="#F57C00", border_width=2)
        btn_frame.pack(fill="x", pady=(4, 0), padx=1, ipady=2, ipadx=2)
        ctk.CTkButton(
            btn_frame, text="Refresh Status", command=self._update_status_labels, width=120,
            fg_color="#444c56", hover_color="#F57C00", text_color="#FFA726"
        ).pack(side="right", padx=(0, 4))

    def refresh_ports(self):
        """
        Refresh the list of available serial ports and update the port selection combobox.
        Enables or disables the connect button based on port availability.
        """
        ports = SerialComUtils.get_port_names()
        if self.combobox:
            self.combobox.configure(values=ports)
            self.combobox.set(self.com_port if self.com_port in ports else (ports[0] if ports else ""))
        if self.conn_btn:
            self.conn_btn.configure(state="normal" if ports else "disabled")

    def _toggle_connection(self):
        """
        Handle connect/disconnect button click.
        Starts a background thread to connect or disconnect from the relay controller.
        """
        if self.controller:
            self._run_in_thread(self._disconnect_threaded)
        else:
            if self.conn_btn:
                self.conn_btn.configure(state="disabled", text="Connecting...")
            self._run_in_thread(self._connect_threaded)

    def _connect_threaded(self):
        """
        Attempt to connect to the relay controller in a background thread.
        On success, updates the UI and relay status. On failure, shows an error dialog.
        """
        port = self.combobox.get() if self.combobox else ""
        try:
            if self.controller:
                self.controller.close()
                self.controller = None
            controller = RelayController(port, switch_delay=0.1)
            statuses = controller.get_statuses()  # <-- FIXED
            if statuses:
                self.root.after(0, self._on_connect_success, controller, port)
            else:
                raise Exception("Failed to read relay status after connecting.")
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            self.root.after(0, lambda: messagebox.showerror("Connection Error", str(e)))
            self.root.after(0, self._update_ui)
        finally:
            self.root.after(0, self._enable_connect_btn)

    def _disconnect_threaded(self):
        """
        Disconnect from the relay controller in a background thread.
        Updates the UI and enables the connect button after disconnecting.
        """
        try:
            if self.controller:
                self.controller.close()
                self.controller = None
        except Exception as e:
            logging.error(f"Disconnection failed: {e}")
            self.root.after(0, lambda: messagebox.showerror("Disconnection Error", str(e)))
        finally:
            self.root.after(0, self._update_ui)
            self.root.after(0, self._enable_connect_btn)

    def _on_connect_success(self, controller: RelayController, port: str):
        """
        Callback for successful connection.
        Sets the controller, updates the UI, and refreshes relay statuses.

        Args:
            controller (RelayController): The connected relay controller instance.
            port (str): The COM port used for connection.
        """
        self.controller = controller
        self.com_port = port
        self._update_ui()
        self._update_status_labels()

    def _enable_connect_btn(self):
        """
        Enable the connect/disconnect button after a connection or disconnection attempt.
        Updates the button text based on connection state.
        """
        if self.conn_btn:
            self.conn_btn.configure(state="normal", text="Disconnect" if self.controller else "Connect")

    def _toggle_relay(self, relay_number: int):
        """
        Toggle the state of a relay in a background thread.

        Args:
            relay_number (int): The relay number to toggle (1-4).
        """
        if self.controller:
            self._run_in_thread(lambda: self._toggle_relay_worker(relay_number))

    def _toggle_relay_worker(self, relay_number: int):
        """
        Worker function to toggle relay state.
        Reads current status and switches relay ON/OFF accordingly.

        Args:
            relay_number (int): The relay number to toggle (1-4).
        """
        try:
            statuses = self.controller.get_statuses()
            relay_key = f"R{relay_number}"
            if statuses.get(relay_key) == "ON":
                self.controller.turn_off(relay_number)  # <-- FIXED
            else:
                self.controller.turn_on(relay_number)   # <-- FIXED
        except Exception as e:
            self.root.after(0, lambda e=e: messagebox.showerror("Relay Error", str(e)))
        self.root.after(0, self._update_status_labels)

    def _update_status_labels(self):
        """
        Update the relay button labels and colors to reflect current relay states.
        If not connected, sets all buttons to unknown state.
        """
        if self.controller:
            try:
                statuses = self.controller.get_statuses()  # <-- FIXED
                for i in range(4):
                    status = statuses.get(f"R{i+1}", "Unknown")
                    color = "green" if status == "ON" else "red" if status == "OFF" else "gray"
                    text = status if status in ("ON", "OFF") else "?"
                    self.relay_buttons[i].configure(text=text, fg_color=color)
            except Exception as e:
                messagebox.showerror("Status Error", str(e))
                for btn in self.relay_buttons:
                    btn.configure(text="?", fg_color="gray")
        else:
            for btn in self.relay_buttons:
                btn.configure(text="?", fg_color="gray")

    def _update_ui(self):
        """
        Update the UI elements (button states, labels) based on connection state.
        Disables relay buttons if not connected.
        """
        is_connected = self.controller is not None
        if self.conn_btn:
            self.conn_btn.configure(
                text="Disconnect" if is_connected else "Connect",
                fg_color="green" if is_connected else "gray"
            )
        for btn in self.relay_buttons:
            btn.configure(state="normal" if is_connected else "disabled")

    def _run_in_thread(self, func):
        """
        Run a function in a background thread to avoid blocking the UI.

        Args:
            func (Callable): The function to run in a thread.
        """
        threading.Thread(target=func, daemon=True).start()

    def run(self):
        """
        Start the GUI main loop. Call this method to launch the application.
        """
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Unexpected error: {e}")

    def close(self):
        """
        Close the GUI and release resources.
        Closes the relay controller connection and destroys the main window.
        """
        if self.controller:
            self.controller.close()
            self.controller = None
        if self.root.winfo_exists():
            self.root.destroy()

    def __del__(self):
        """
        Destructor to ensure resources are released when the object is deleted.
        """
        try:
            self.close()
        except Exception:
            pass

def main():
    """
    Entry point for running the GUI as a standalone application.
    """
    print("\n--- KMTronic USB Relay Controller GUI ---")
    RelayControllerGui().run()

if __name__ == "__main__":
    main()
