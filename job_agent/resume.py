from pathlib import Path
from pypdf import PdfReader
from .rag import index_document

def extract_resume_text(pdf_path):
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(path)
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    if not text:
        raise ValueError("No selectable text found. This may be a scanned PDF; OCR is not included.")
    return text

def ingest_resume(pdf_path):
    text = extract_resume_text(pdf_path)
    count = index_document(
        text=text,
        doc_id="candidate-resume",
        source="resume",
        metadata={"document_type": "candidate_resume"}
    )
    return text, count
