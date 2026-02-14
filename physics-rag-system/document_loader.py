"""
PDF Document Loader
Extracts text, formulas, metadata, and page numbers.
"""

import fitz  # PyMuPDF


def load_pdf(file_path: str):
    """
    Loads PDF and returns list of dict:
    [
        {
            "content": text,
            "page": page_number,
            "metadata": {...}
        }
    ]
    """

    doc = fitz.open(file_path)
    documents = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")

        documents.append({
            "content": text,
            "page": page_num,
            "metadata": {
                "page_number": page_num,
                "source": file_path
            }
        })

    return documents
