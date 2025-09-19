import socket
import gradio as gr

from py_uds_demo.core.client import UdsClient


class Web:
    """
    WebUi provides a Gradio-based web interface for interacting with the UDS (Unified Diagnostic Services) simulator.

    This class manages the UI components, handles user input, processes diagnostic requests, and logs interactions.
    """

    def __init__(self):
        """
        Initialize the WebUi instance.

        Sets up the UdsClient and default log file path.
        """
        self.uds_client = UdsClient()
        self.logger = self.uds_client.server.logger

    def run(self):
        """
        Launch the Gradio app for the UDS simulator UI.

        Initializes the logger and starts the Gradio Blocks interface.
        """
        uds_sim = gr.Blocks(title="UDS Simulator")
        with uds_sim:
            self.uds_simulator_ui()
        uds_sim.launch(server_name=socket.getfqdn(), server_port=7865, share=False, debug=False)

    def uds_simulator_ui(self):
        """
        Build the Gradio UI for the UDS simulator.

        Sets up the tester present checkbox, chatbot, and diagnostic request textbox.
        """
        self.tester_present_checkbox = gr.Checkbox(label="tester_present", value=False)
        self.uds_sim_chatbot = gr.Chatbot(type="messages", label="UDS Simulator(Chat Box)", show_label=True, show_copy_all_button=True, layout="bubble", value=[])
        self.diag_req_textbox = gr.Textbox(label="Diagnostic Request", placeholder="Enter diagnostic request in hex format (e.g., 22 F1 87). No need to mention size.", show_label=True)
        self.diag_req_textbox.submit(self.chat_bot_process, [self.diag_req_textbox, self.uds_sim_chatbot], [self.diag_req_textbox, self.uds_sim_chatbot])
        self.tester_present_checkbox.change(self._update_tester_present, [self.tester_present_checkbox])

        with gr.Row():
            self.help_sid_textbox = gr.Textbox(label="Help with SID", placeholder="Enter SID (e.g., 10)", show_label=True)
            self.help_button = gr.Button(value="Get Help")
        self.help_button.click(self._show_help_callback, [self.help_sid_textbox, self.uds_sim_chatbot], [self.help_sid_textbox, self.uds_sim_chatbot])

    def _show_help_callback(self, sid_str, chat_history):
        try:
            sid = int(sid_str, 16)
            service = self.uds_client.server.service_map.get(sid)
            if service:
                chat_history.append({"role": "user", "content": f"Help for SID 0x{sid:02X}"})
                chat_history.append({"role": "assistant", "content": service.__doc__})
            else:
                chat_history.append({"role": "user", "content": f"Help for SID 0x{sid:02X}"})
                chat_history.append({"role": "assistant", "content": f"No help found for SID 0x{sid:02X}."})
        except (ValueError, IndexError):
            chat_history.append({"role": "user", "content": f"Help for SID {sid_str}"})
            chat_history.append({"role": "assistant", "content": "Invalid SID. Please enter a valid hex value."})
        return "", chat_history

    def chat_bot_process(self, diagnostic_request, chat_history):
        """
        Process user diagnostic request and update chat history.

        Args:
            diagnostic_request (str): The diagnostic request input by the user in hex string format.
            chat_history (list): The current chat history between user and assistant.

        Returns:
            tuple: A tuple of (empty string, updated chat_history).
        """
        diagnostic_request_clean = diagnostic_request.replace(" ", "")
        try:
            diagnostic_request_stream = [int(diagnostic_request_clean[i:i+2], 16) for i in range(0, len(diagnostic_request_clean), 2)]
            user_sent_request = self.uds_client.format_request(diagnostic_request_stream)
            chat_history.append({"role": "user", "content": user_sent_request})
            diagnostic_response = self.uds_client.send_request(diagnostic_request_stream, True)
            chat_history.append({"role": "assistant", "content": diagnostic_response})
        except ValueError:
            chat_history.append({"role": "user", "content": diagnostic_request})
            chat_history.append({"role": "assistant", "content": "Invalid hex input. Please enter a valid hex string."})
            self.logger.warning(f"Invalid Diagnostic Request 💉 {diagnostic_request}")
        except Exception as e:
            chat_history.append({"role": "user", "content": diagnostic_request})
            chat_history.append({"role": "assistant", "content": f"An error occurred while processing the request. {e}"})
            self.logger.error(f"Error occurred while processing request 💉 {diagnostic_request}: {e}")
        finally:
            return "", chat_history

    def _update_tester_present(self, value: bool):
        """
        Update the tester present flag in the UDS server and log the action.

        Args:
            value (bool): True to activate tester present, False to deactivate.
        """
        self.uds_client.server.diagnostic_session_control.tester_present_active = value
        self.logger.info('tester present [✔️] activated' if value else 'tester present [✖️] deactivated')


if __name__ == "__main__":
    web_ui = Web()
    web_ui.run()
