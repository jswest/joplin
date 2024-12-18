import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)

embedder = Embedder()

def get_embeddings(texts: List[str]) -> np.ndarray:
    return embedder.get_embeddings(texts)