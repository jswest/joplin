from typing import List, Tuple

from .pdf import extract_text_from_pdf
from .text import chunk_text

def process_document(file_path: str) -> Tuple[str, List[str]]:
    if file_path.endswith('.pdf'):
        full_text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.md') or file_path.endswith('txt'):
        with open(file_path, 'r') as in_file:
            full_text = in_file.read()
    else:
        raise ValueError(f"Unsupported file type: {file_path.split('.')[-1]}")
    
    chunks = chunk_text(full_text)
    
    return full_text, chunks