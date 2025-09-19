import streamlit as st
import canmatrix
import canmatrix.formats
import io
from typing import Optional, Any, Dict, Tuple

class WebApp:
    """
    Streamlit-based web application for interacting with CAN matrix files using the canmatrix package.

    Features:
        - Upload CAN matrix files in various formats (DBC, ARXML, KCD, FIBEX, XLS, XLSX, XML).
        - Explore loaded matrices, view ECUs, frames, and signals.
        - Export matrices to supported formats.
    """

    def __init__(self) -> None:
        """
        Initialize the WebApp instance.
        """
        self.cm: Optional[Dict[str, Any]] = None

    def run(self) -> None:
        """
        Main entry point for the Streamlit web application.
        """
        st.title("Canmatrix WebApp")
        st.write(
            "Interact with CAN matrix files using the "
            "[canmatrix](https://github.com/ebroecker/canmatrix) package."
        )
        self.load_matrix_ui()
        if self.cm:
            self.explore_matrices_ui()

    @staticmethod
    @st.cache_data(show_spinner="Loading CAN matrix file...")
    def load_canmatrix_file(file_bytes: bytes, file_format: str) -> Tuple[Optional[Dict[str, Any]], Any]:
        """
        Load a CAN matrix file using canmatrix.formats.load and normalize the result.

        Args:
            file_bytes (bytes): The file content as bytes.
            file_format (str): The format of the CAN matrix file.

        Returns:
            Tuple[Optional[Dict[str, Any]], Any]: Tuple of (matrices dict or None, loaded raw object).
        """
        file_like = io.BytesIO(file_bytes)
        loaded = canmatrix.formats.load(
            file_like,
            import_type=file_format,
            file_format=file_format
        )

        matrices: Optional[Dict[str, Any]] = None
        if isinstance(loaded, dict):
            matrices = loaded
        elif hasattr(loaded, "matrices"):
            matrices = loaded.matrices

        # Assign default names to unnamed matrices (common in ARXML)
        if matrices:
            matrices = {
                name if name else f"Matrix_{idx+1}": matrix
                for idx, (name, matrix) in enumerate(matrices.items())
            }
        return matrices, loaded

    def load_matrix_ui(self) -> None:
        """
        UI for uploading and loading a CAN matrix file.
        """
        st.header("1. Load CAN Matrix File")
        uploaded_file = st.file_uploader(
            "Upload a CAN matrix file (DBC, ARXML, KCD, FIBEX, XLS, XLSX, ...)",
            type=["dbc", "arxml", "kcd", "fibex", "xml", "xls", "xlsx"]
        )
        if uploaded_file:
            file_format = st.selectbox(
                "Select file format",
                options=["dbc", "arxml", "kcd", "fibex", "xls", "xlsx", "xml"]
            )
            try:
                file_bytes = uploaded_file.read()
                matrices, loaded = self.load_canmatrix_file(file_bytes, file_format)
                if matrices and len(matrices) > 0:
                    st.success(f"Loaded CAN matrix with {len(matrices)} matrix/matrices.")
                    self.cm = matrices  # store matrices dict for later use
                else:
                    st.warning("Loaded file, but no matrices found.")
                    st.info(f"Type of loaded object: {type(loaded)}")
                    st.info(f"Loaded object: {loaded}")
            except Exception as e:
                st.error(f"Failed to load file: {e}")

    def explore_matrices_ui(self) -> None:
        """
        UI for exploring loaded matrices and exporting them.
        """
        st.header("2. Explore Matrices")
        if not self.cm or not isinstance(self.cm, dict):
            st.warning("No matrices found in the loaded file.")
            return
        matrix_names = list(self.cm.keys())
        if not matrix_names:
            st.warning("No matrices found in the loaded file.")
            return

        matrix_name = st.selectbox("Select Matrix", matrix_names)
        matrix = self.cm[matrix_name]

        self.display_matrix_info(matrix)
        self.display_frames_ui(matrix)
        self.export_matrix_ui(matrix)

    def display_matrix_info(self, matrix: Any) -> None:
        """
        Display basic information about the selected matrix.

        Args:
            matrix (Any): The CAN matrix object to display information for.
        """
        st.subheader("Matrix Info")
        name = getattr(matrix, 'name', 'N/A')
        ecus = getattr(matrix, 'ecus', [])
        frames = getattr(matrix, 'frames', [])
        num_signals = sum(len(frame.signals) for frame in frames)
        st.write(f"Name: {name}")
        st.write(f"ECUs: {', '.join([ecu.name for ecu in ecus]) if ecus else 'None'}")
        st.write(f"Frames: {len(frames)}")
        st.write(f"Signals: {num_signals}")

    def display_frames_ui(self, matrix: Any) -> None:
        """
        UI for selecting and displaying frame details.

        Args:
            matrix (Any): The CAN matrix object containing frames.
        """
        st.subheader("Frames")
        frames = getattr(matrix, "frames", [])
        frame_names = [frame.name for frame in frames]
        if not frame_names:
            st.info("No frames available in this matrix.")
            return

        selected_frame = st.selectbox("Select Frame", frame_names)
        frame = next((f for f in frames if f.name == selected_frame), None)
        if frame:
            frame_id = getattr(getattr(frame, "arbitration_id", None), "id", None)
            st.write(f"Frame ID: {hex(frame_id) if frame_id is not None else 'N/A'}")
            st.write(f"Signals: {[signal.name for signal in getattr(frame, 'signals', [])]}")
        else:
            st.warning("Selected frame not found.")

    @staticmethod
    @st.cache_data(show_spinner="Exporting matrix...")
    def export_matrix_to_bytes(matrix: Any, export_format: str) -> bytes:
        """
        Export a CAN matrix to the specified format and return as bytes.

        Args:
            matrix (Any): The CAN matrix object to export.
            export_format (str): The export format (e.g., 'dbc', 'arxml', etc.).

        Returns:
            bytes: The exported file content.
        """
        out = io.BytesIO()
        canmatrix.formats.dump(matrix, out, export_format)
        out.seek(0)
        return out.read()

    def export_matrix_ui(self, matrix: Any) -> None:
        """
        UI for exporting the selected matrix to a chosen format.

        Args:
            matrix (Any): The CAN matrix object to export.
        """
        st.subheader("Export Matrix")
        export_format = st.selectbox(
            "Export Format",
            ["dbc", "arxml", "kcd", "fibex", "xls", "xlsx", "xml"]
        )
        if st.button("Export"):
            try:
                data = self.export_matrix_to_bytes(matrix, export_format)
                st.download_button(
                    label=f"Download {export_format.upper()}",
                    data=data,
                    file_name=f"{getattr(matrix, 'name', 'matrix')}.{export_format}"
                )
            except Exception as e:
                st.error(f"Export failed: {e}")

if __name__ == "__main__":
    WebApp().run()