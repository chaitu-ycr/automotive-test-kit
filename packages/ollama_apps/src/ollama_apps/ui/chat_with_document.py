import gradio as gr
from typing import Callable, List, Dict, Any, Generator, Optional

class GradioChatWithDocumentTab:
    """
    Gradio tab for chatting with uploaded documents.
    """

    def __init__(self, chat_with_document_function: Callable[[Any, str], Generator[str, None, None]]):
        """
        Args:
            chat_with_document_function: Function that takes a file and a question,
                                         and yields response chunks as strings.
        """
        self.chat_function = chat_with_document_function
        self.tab_title = "Chat with Documents"
        self.elem_id = "document_chatbot"

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
        """Create the Gradio tab UI for document chat."""
        with gr.Blocks() as tab:
            gr.Markdown(f"### {self.tab_title} (Streaming Responses)")
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = self.create_chatbot()
                    question_input = gr.Textbox(
                        placeholder="Ask a question about the document...",
                        show_label=False
                    )
                with gr.Column(scale=1):
                    file_input = gr.File(label="Upload Document")
                    file_state = gr.State(None)

            file_input.upload(
                lambda file: file,
                inputs=file_input,
                outputs=file_state
            )

            question_input.submit(
                self.respond,
                inputs=[file_state, question_input, chatbot],
                outputs=chatbot
            )
        return tab

    def respond(
        self,
        file: Optional[Any],
        question: str,
        chat_history: Optional[List[Dict[str, str]]]
    ) -> Generator[List[Dict[str, str]], None, None]:
        """
        Handles user input and streams assistant responses.

        Args:
            file: Uploaded file object from state.
            question: User's question.
            chat_history: List of previous chat messages.

        Yields:
            Updated chat history after each streamed response chunk.
        """
        chat_history = chat_history or []

        if not file:
            yield chat_history + [{"role": "assistant", "content": "Please upload a document first."}]
            return
        if not question:
            yield chat_history + [{"role": "assistant", "content": "Please enter a question."}]
            return

        chat_history.append({"role": "user", "content": self._format_user_input(file, question)})

        response = ""
        assistant_idx = len(chat_history)
        chat_history.append({"role": "assistant", "content": ""})
        try:
            for chunk in self.chat_function(file, question):
                response += chunk
                chat_history[assistant_idx]["content"] = response
                yield chat_history
        except Exception as e:
            chat_history[assistant_idx]["content"] = f"Error: {e}"
            yield chat_history

    @staticmethod
    def _format_user_input(file: Any, question: str) -> str:
        """
        Formats the user's input for display in the chat.

        Args:
            file: Uploaded file object.
            question: User's question.

        Returns:
            Formatted string for chat display.
        """
        name = getattr(file, "name", str(file)) if file else ""
        if name and question:
            return f"Uploaded file: {name}\n{question}"
        if name:
            return f"Uploaded file: {name}"
        return question or ""