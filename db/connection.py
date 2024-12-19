import chromadb
from contextlib import contextmanager

def get_db():
    return chromadb.PersistentClient(path="./db/chroma")

def init_db():
    client = get_db()
    client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )
    client.get_or_create_collection(
        name="chunks",
        metadata={"hnsw:space": "cosine"}
    )