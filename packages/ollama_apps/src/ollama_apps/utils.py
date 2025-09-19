import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List, Optional, Callable

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ollama_apps.utils")

def log_message(message: str, level: str = "info") -> None:
    """
    Log a message with the specified log level.

    Args:
        message: The message to log.
        level: The log level ("info", "warning", "error", "debug").
    """
    level = level.lower()
    log_func = getattr(logger, level, logger.info)
    log_func(message)

def load_documents_parallel(
    files: List[Any],
    loader_func: Optional[Callable[[str], Any]] = None
) -> List[Any]:
    """
    Load multiple documents in parallel.

    Args:
        files: List of file-like objects with a 'name' attribute.
        loader_func: Optional custom loader function. If None, tries to import DocumentLoader.

    Returns:
        List of loaded documents (one per file, order preserved).
    """
    if loader_func is None:
        try:
            from ollama_apps.core import DocumentLoader
            loader_func = DocumentLoader.load
        except ImportError:
            raise RuntimeError("DocumentLoader could not be imported.")

    results: List[Any] = [None] * len(files)
    with ThreadPoolExecutor() as executor:
        future_to_idx = {
            executor.submit(loader_func, getattr(file, "name", str(file))): idx
            for idx, file in enumerate(files)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as exc:
                log_message(f"Error loading document: {exc}", level="error")
                results[idx] = []
    return results