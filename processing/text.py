import hashlib
import ollama
from typing import List

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence_size = len(sentence)
        if current_size + sentence_size > chunk_size and current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentence]
            current_size = sentence_size
        else:
            current_chunk.append(sentence)
            current_size += sentence_size
    
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return chunks

def hash_text(text: str, algorithm: str = "sha256") -> str:
    text_bytes = text.encode("utf-8")
    hash = hashlib.new(algorithm)
    hash.update(text_bytes)
    return hash.hexdigest()

def summarize_chunk(chunk: str, model: str = "mistral") -> str:
    response = ollama.generate(
        model=model,
        prompt=f"Summarize the following text:\n\n{chunk}\n\nSummary:"
    )
    return response["response"]

def summarize_document(text: str, target_length: int = 500, model: str = "mistral") -> str:
    current_text = text
    while len(current_text.split()) > target_length:
        chunks = chunk_text(current_text, chunk_size=3000)
        summaries = [summarize_chunk(chunk, model=model) for chunk in chunks]
        current_text = " ".join(summaries)
    return current_text
