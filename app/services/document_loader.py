from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)


class DocumentLoader:

    def load(self, file_path: str):
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return PyPDFLoader(str(path)).load()

        elif suffix in {".txt", ".md"}:
            try:
                return TextLoader(
                    str(path),
                    encoding="utf-8"
                ).load()
            except Exception:
                return TextLoader(
                    str(path),
                    encoding="cp1252"
                ).load()

        elif suffix == ".docx":
            return UnstructuredWordDocumentLoader(
                str(path)
            ).load()

        else:
            raise ValueError(
                f"Unsupported file type: {suffix}"
            )
