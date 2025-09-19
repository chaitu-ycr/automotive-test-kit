from langchain_community.document_loaders import PyPDFLoader
from langchain_unstructured import UnstructuredLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from ollama_apps.utils import log_message
from typing import List, Any, Generator, Optional
from functools import lru_cache
from hashlib import sha256


class DocumentLoader:
    """
    Handles loading documents from various file formats.
    """

    @staticmethod
    @lru_cache(maxsize=50)
    def load(file_path: str) -> List[Any]:
        """
        Load a document from a file path.
        """
        log_message(f"Loading document: {file_path}")
        try:
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = UnstructuredLoader(file_path)
            return loader.load()
        except Exception as e:
            log_message(f"Error loading file {file_path}: {e}", level="error")
            return []


class EmbeddingsManager:
    """
    Singleton for managing HuggingFace embeddings.
    """
    _cached_embeddings: Optional[HuggingFaceEmbeddings] = None

    @classmethod
    def get_embeddings(cls) -> HuggingFaceEmbeddings:
        if cls._cached_embeddings is None:
            log_message("Initializing embeddings...")
            cls._cached_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return cls._cached_embeddings


class VectorStore:
    """
    Manages the FAISS vector store for document retrieval.
    """

    def __init__(self, embeddings: HuggingFaceEmbeddings):
        self.embeddings = embeddings
        self.db = None

    def add_documents(self, documents: List[Any], batch_size: int = 100) -> None:
        if not documents:
            raise ValueError("No documents provided to add to the vector store.")
        log_message(f"Adding {len(documents)} documents to the vector store...")
        if self.db is None:
            self.db = FAISS.from_documents(documents, self.embeddings)
        else:
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                self.db.add_documents(batch)

    def as_retriever(self) -> Any:
        if self.db is None:
            raise ValueError("No documents have been added to the vector store.")
        return self.db.as_retriever()

    def clear(self) -> None:
        self.db = None


class QARetrievalChain:
    """
    Handles retrieval-augmented QA using a retriever and LLM.
    """
    _cached_chain = None

    def __init__(self, llm: OllamaLLM, retriever: Any):
        if QARetrievalChain._cached_chain is None:
            log_message("Initializing QA retrieval chain...")
            QARetrievalChain._cached_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        self.chain = QARetrievalChain._cached_chain
        self.llm = llm
        self.retriever = retriever

    def stream(self, query: str) -> Generator[str, None, None]:
        """
        Stream the QA chain response for a query.
        """
        log_message(f"Streaming query: {query}")
        try:
            docs = self.retriever.get_relevant_documents(query)
            context = "\n\n".join(doc.page_content for doc in docs)
            prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
            for chunk in self.llm.stream(prompt):
                yield chunk
        except Exception as e:
            log_message(f"Error running QA chain (stream): {e}", level="error")
            yield f"An error occurred: {e}"

    def invoke(self, query: str) -> str:
        """
        Run the QA chain with a query and return the answer.
        """
        log_message(f"Processing query: {query}")
        try:
            result = self.chain.invoke(query)
            if isinstance(result, dict):
                for key in ("result", "answer", "output"):
                    if key in result:
                        return result[key]
                return next(iter(result.values()))
            return result
        except Exception as e:
            log_message(f"Error running QA chain: {e}", level="error")
            raise


class ChatWithDocument:
    """
    Handles chat interactions with uploaded documents.
    """

    def __init__(self):
        self.embeddings_manager = EmbeddingsManager()
        self.vector_store: Optional[VectorStore] = None
        self._cached_file_hash: Optional[str] = None

    def chat(self, file: Any, query: str) -> Generator[str, None, None]:
        """
        Process a chat query with a document and stream the response.
        """
        try:
            file_bytes = self._get_file_bytes(file)
            file_hash = sha256(file_bytes).hexdigest()

            # Reload vector store only if the file has changed
            if self.vector_store is None or self._cached_file_hash != file_hash:
                docs = DocumentLoader.load(getattr(file, "name", file))
                if not docs:
                    yield "No content found in the uploaded document."
                    return
                embeddings = self.embeddings_manager.get_embeddings()
                self.vector_store = VectorStore(embeddings)
                self.vector_store.add_documents(docs)
                self._cached_file_hash = file_hash

            retriever = self.vector_store.as_retriever()
            llm = OllamaLLM(model="llama3.2", streaming=True)
            qa_chain = QARetrievalChain(llm, retriever)
            yield from self._stream_response(qa_chain, query)
        except Exception as e:
            log_message(f"Error in chat_with_document: {e}", level="error")
            yield f"An error occurred: {e}"

    @staticmethod
    def _get_file_bytes(file: Any) -> bytes:
        if hasattr(file, "read"):
            file_bytes = file.read()
            file.seek(0)
            return file_bytes
        if hasattr(file, "decode"):
            decoded = file.decode()
            return decoded if isinstance(decoded, bytes) else decoded.encode()
        if isinstance(file, str):
            with open(file, "rb") as f:
                return f.read()
        raise ValueError("Unsupported file object type for hashing.")

    @staticmethod
    def _stream_response(qa_chain: QARetrievalChain, query: str, buffer_size: int = 3) -> Generator[str, None, None]:
        buffer = []
        for chunk in qa_chain.stream(query):
            buffer.append(chunk)
            if len(buffer) >= buffer_size:
                yield "".join(buffer)
                buffer = []
        if buffer:
            yield "".join(buffer)


class ChatWithModel:
    """
    Handles chat interactions with Ollama models.
    """

    def __init__(self, model_name: str = "llama3.2"):
        self.llm = OllamaLLM(model=model_name, streaming=True)

    def chat(self, query: str) -> Generator[str, None, None]:
        """
        Process a chat query with the Ollama model and stream the response.
        """
        log_message(f"Processing query with Ollama model: {query}")
        try:
            buffer = []
            for chunk in self.llm.stream(query):
                buffer.append(chunk)
                if len(buffer) >= 3:
                    yield "".join(buffer)
                    buffer = []
            if buffer:
                yield "".join(buffer)
        except Exception as e:
            log_message(f"Error in chat_with_model: {e}", level="error")
            yield f"An error occurred: {e}"