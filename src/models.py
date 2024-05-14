from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class PDFDocument:
    filename: str
    content: str

class PDFModel(BaseModel):
    filename: str
    content: str