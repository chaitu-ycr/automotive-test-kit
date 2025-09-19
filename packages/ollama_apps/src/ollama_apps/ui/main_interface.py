import gradio as gr
from typing import Callable, Optional, Generator, Any
from ollama_apps.ui.chat_with_model import GradioChatWithModelTab
from ollama_apps.ui.chat_with_document import GradioChatWithDocumentTab

class GradioInterface:
    """
    Main Gradio interface with tabs for model and document chat.
    """

    def __init__(
        self,
        chat_with_document_function: Callable[[Any, str], Generator[str, None, None]],
        chat_with_model_function: Callable[[str], Generator[str, None, None]],
    ):
        """
        Initialize the Gradio interface with chat functions.
        """
        self._tabs = (
            GradioChatWithModelTab(chat_with_model_function),
            GradioChatWithDocumentTab(chat_with_document_function),
        )
        self._interface: Optional[gr.Blocks] = None

    def _build_interface(self) -> gr.Blocks:
        """
        Build and cache the Gradio Blocks interface with all tabs.
        """
        if self._interface:
            return self._interface
        with gr.Blocks() as interface:
            for tab in self._tabs:
                with gr.Tab(tab.tab_title):
                    tab.create_tab()
        self._interface = interface
        return interface

    def launch(self) -> None:
        """
        Launch the Gradio interface.
        """
        if not self._interface:
            self._build_interface()
        self._interface.launch()