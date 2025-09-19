"""
Main entry point for the Ollama app.
"""

from typing import Optional
from ollama_apps.core import ChatWithDocument, ChatWithModel
from ollama_apps.ui.main_interface import GradioInterface

__all__ = ["OllamaApp"]


class OllamaApp:
    """
    Main application class for the Ollama app.
    Initializes chat handlers and the Gradio interface.
    """

    __slots__ = ("chat_with_document_handler", "chat_with_model_handler", "interface")

    def __init__(
        self,
        chat_with_document_handler: Optional[ChatWithDocument] = None,
        chat_with_model_handler: Optional[ChatWithModel] = None,
        interface: Optional[GradioInterface] = None,
    ):
        self.chat_with_document_handler = chat_with_document_handler or ChatWithDocument()
        self.chat_with_model_handler = chat_with_model_handler or ChatWithModel()
        self.interface = interface or GradioInterface(
            chat_with_document_function=self.chat_with_document_handler.chat,
            chat_with_model_function=self.chat_with_model_handler.chat,
        )

    def run(self) -> None:
        """Launch the Gradio interface."""
        self.interface.launch()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"chat_with_document_handler={repr(self.chat_with_document_handler)}, "
            f"chat_with_model_handler={repr(self.chat_with_model_handler)}, "
            f"interface={repr(self.interface)})"
        )

    def __str__(self) -> str:
        return f"{self.__class__.__name__} app with Gradio interface"


def main() -> None:
    """Run the Ollama app."""
    OllamaApp().run()


if __name__ == "__main__":
    main()