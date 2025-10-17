from pathlib import Path
from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders import PyMuPDFLoader
import shutil


class FileLoader:
    """
    Unified file loader for PDF or TXT.
    PDFs are saved in `data/raw`, extracted text (or TXT file) is saved in `data/texts`.
    """

    def __init__(self, file_path: str):
        self.original_path = Path(file_path)
        if not self.original_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Base data folder relative to current working directory
        self.data_dir = Path.cwd() / "data"
        self.raw_dir = self.data_dir / "raw"
        self.text_dir = self.data_dir / "texts"

        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.text_dir.mkdir(parents=True, exist_ok=True)

        # Decide where to save the original file
        if self.original_path.suffix.lower() == ".pdf":
            self.saved_path = self.raw_dir / self.original_path.name
        elif self.original_path.suffix.lower() == ".txt":
            self.saved_path = self.text_dir / self.original_path.name
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT are supported.")

        # Copy original file
        shutil.copy(str(self.original_path), str(self.saved_path))

        # Set path for output TXT (always saved in texts/)
        self.output_text_path = self.text_dir / f"{self.original_path.stem}.txt"

    def load(self) -> List[Document]:
        ext = self.saved_path.suffix.lower()

        if ext == ".pdf":
            # Extract text from PDF
            loader = PyMuPDFLoader(str(self.saved_path))
            docs = loader.load()
            full_text = "\n\n".join([d.page_content for d in docs])
        else:  # TXT
            with open(self.saved_path, "r", encoding="utf-8", errors="ignore") as f:
                full_text = f.read()
            docs = [Document(page_content=full_text)]

        # Save extracted text as TXT in texts folder
        self.output_text_path.write_text(full_text, encoding="utf-8")

        # Strip whitespace from docs
        for doc in docs:
            doc.page_content = doc.page_content.strip()

        return docs
