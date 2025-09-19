import gradio as gr
from typing import Callable, List, Dict, Any, Generator, Optional

class GradioChatWithModelTab:
    """
    Gradio tab for chatting with local Ollama models.
    """

    def __init__(self, chat_with_model_function: Callable[[str], Generator[str, None, None]]):
        """
        Args:
            chat_with_model_function: Function that takes a user message and yields response chunks.
        """
        self.chat_function = chat_with_model_function
        self.tab_title = "Chat with Local Models"
        self.elem_id = "chatbot"

    def create_chatbot(self) -> gr.Chatbot:
        """Create and return a Gradio Chatbot component."""
        return gr.Chatbot(
            elem_id=self.elem_id,
            bubble_full_width=False,
            type="messages",
            resizable=True,
            show_copy_button=True,
            show_copy_all_button=True,
            height=600,
        )

    def create_tab(self) -> gr.Blocks:
        """Create the Gradio tab UI for model chat."""
        with gr.Blocks() as tab:
            gr.Markdown(f"### {self.tab_title} (Streaming Responses)")
            chatbot = self.create_chatbot()
            msg_input = gr.MultimodalTextbox(
                interactive=True,
                file_count="multiple",
                placeholder="Enter message or upload file...",
                show_label=False,
                sources=["microphone", "upload"],
            )
            msg_input.submit(
                self.respond,
                inputs=[msg_input, chatbot],
                outputs=chatbot
            )
        return tab

    def respond(
        self,
        message: Dict[str, Any],
        chat_history: Optional[List[Dict[str, Any]]]
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Handles user input and streams assistant responses.

        Args:
            message: Dict with keys 'text' and 'files' from MultimodalTextbox.
            chat_history: List of previous chat messages.

        Yields:
            Updated chat history after each streamed response chunk.
        """
        chat_history = chat_history or []

        user_text = message.get("text", "")
        files = message.get("files", [])

        if not user_text and not files:
            yield chat_history
            return

        user_content = []
        if files:
            file_names = ", ".join(getattr(f, "name", str(f)) for f in files)
            user_content.append(f"Uploaded files: {file_names}")
        if user_text:
            user_content.append(user_text)
        if user_content:
            chat_history.append({"role": "user", "content": "\n".join(user_content)})

        if user_text:
            response = ""
            assistant_index = len(chat_history)
            chat_history.append({"role": "assistant", "content": ""})
            try:
                for chunk in self.chat_function(user_text):
                    response += chunk
                    chat_history[assistant_index]["content"] = response
                    yield chat_history
            except Exception as e:
                chat_history[assistant_index]["content"] = f"Error: {e}"
                yield chat_history
        else:
            yield chat_history