from dearpygui import dearpygui as dpg
from py_uds_demo.core.client import UdsClient

class Gui:
    def __init__(self):
        self.client = UdsClient()
        self._setup_ui()

    def _setup_ui(self):
        dpg.create_context()
        dpg.create_viewport(title="UDS Simulation GUI", width=920, height=500)

        with dpg.window(label="UDS Simulation GUI", width=900, height=480, tag="main_window"):
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="Tester Present", callback=self._toggle_tester_present, tag="tester_present_checkbox")

            with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=120):
                with dpg.group(horizontal=True):
                    dpg.add_text("Tx Request")
                    dpg.add_input_text(label="", width=400, tag="request_entry", on_enter=True, callback=self._send_request_callback)
                    dpg.add_button(label="Send", callback=self._send_request_callback)
                dpg.add_text("Rx Response")
                dpg.add_input_text(label="", width=850, height=50, multiline=True, tag="response_textbox", readonly=True)

            with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=120):
                dpg.add_text("History")
                dpg.add_input_text(multiline=True, width=850, height=80, tag="history_textbox", readonly=True)

            with dpg.group(horizontal=True):
                dpg.add_text("Help")
                dpg.add_input_text(label="", width=200, tag="help_entry", hint="Enter SID (e.g., 10)", on_enter=True, callback=self._show_help_callback)
                dpg.add_button(label="Get Help", callback=self._show_help_callback)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def _show_help_callback(self, sender, app_data, user_data):
        sid_str = dpg.get_value("help_entry")
        try:
            sid = int(sid_str, 16)
            service = self.client.server.service_map.get(sid)
            if service:
                title = f"Help for SID 0x{sid:02X}"
                message = service.__doc__ or "No documentation available."
            else:
                title = "Error"
                message = f"No help found for SID 0x{sid:02X}"
        except ValueError:
            title = "Error"
            message = "Invalid SID. Please enter a valid hex value."

        if dpg.does_item_exist("help_modal"):
            dpg.delete_item("help_modal")
        with dpg.window(label=title, modal=True, tag="help_modal", no_close=False, width=700, height=300):
            dpg.add_text(message)
            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("help_modal"))

    def _send_request_callback(self, sender=None, app_data=None, user_data=None):
        request_data = dpg.get_value("request_entry").replace(" ", "")
        try:
            request_data_stream = [int(request_data[i:i+2], 16) for i in range(0, len(request_data), 2)]
            request_data_formatted = " ".join(f"{b:02X}" for b in request_data_stream)
            response_data = self.client.send_request(request_data_stream, False)
            response_data_formatted = " ".join(f"{b:02X}" for b in response_data)
        except ValueError:
            request_data_formatted = f"😡 Invalid input({request_data}). Please enter a valid hex string."
            response_data_formatted = ""
        except Exception as e:
            request_data_formatted = f"😡 An error occurred: {e}"
            response_data_formatted = ""
        dpg.set_value("response_textbox", response_data_formatted)
        current_history = dpg.get_value("history_textbox")
        new_entry = f"-> {request_data_formatted}\n<- {response_data_formatted}\n"
        dpg.set_value("history_textbox", new_entry + current_history)

    def _toggle_tester_present(self, sender, app_data, user_data):
        self.client.server.diagnostic_session_control.tester_present_active = bool(dpg.get_value("tester_present_checkbox"))

if __name__ == "__main__":
    Gui()
