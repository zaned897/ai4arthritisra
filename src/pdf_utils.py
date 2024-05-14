import os
from pathlib import Path
import PyPDF2
from typing import List
from .models import PDFModel

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a pdf file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def load_pdfs_from_directory(directory: str) -> List[PDFModel]:
    """Load PDFs from a directory and extract the text on each PDF."""
    directory_path = Path(directory)
    pdfs_models = []
    for file in directory_path.iterdir():
        if file.suffix == '.pdf':
            pdf_text = extract_text_from_pdf(file)
            pdf_model = PDFModel(filename=file.name, content=pdf_text)
            pdfs_models.append(pdf_model)
    return pdfs_models
