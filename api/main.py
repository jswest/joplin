from fastapi import FastAPI, UploadFile, HTTPException
from pathlib import Path
import tempfile
import shutil
from uuid import uuid4

from .models import Query
from processing import get_embeddings, process_document

from db.connection import get_db

app = FastAPI()

@app.post("/documents/")
async def create_document(file: UploadFile):
    file_extension = file.filename.split('.')[-1]
    file_name = f"{str(uuid4())}.{file_extension}"
    file_path = f"./documents/{file_name}"

    with open(f"./documents/{file_name}", "wb") as out_file:
        shutil.copyfileobj(file.file, out_file)
  
    try:
        full_text, chunks, embeddings = process_document(file_path)
        
        with get_db() as connection:
            cursor = connection.execute(
                """
                INSERT INTO documents (body, file_name, format) 
                VALUES (?, ?, ?)
                RETURNING id
                """,
                (full_text, file_name, file_extension)
            )
            document_id = cursor.fetchone()['id']

            for chunk, embedding in zip(chunks, embeddings):
                connection.execute(
                    """
                    INSERT INTO chunks (body, embedding, document_id)
                    VALUES (?, ?, ?)
                    """,
                    (chunk, embedding.tobytes(), document_id)
                )
        
        return {"id": document_id, "chunks_processed": len(chunks)}
    except Exception as e:
        print(e)

@app.post("/query/")
async def query_documents(query: Query):
    query_embedding = get_embeddings([query.text])[0]
    
    with get_db() as connection:
        results = connection.execute(
            """
            SELECT
                c.id,
                c.created_at,
                c.body,
                d.created_at AS document_created_at,
                d.dek AS document_dek,
                d.file_name as document_file_name,
                d.format AS document_format,
                d.hed AS document_hed,
                d.id AS document_id,
                d.is_note AS document_is_note,
                vss_distance(chunks.embedding, ?) as similarity
            FROM chunks AS c
            JOIN documents AS d ON c.document_id = d.id
            ORDER BY c.embedding <-> ?
            LIMIT 10
            """,
            (
                query_embedding.tobytes(),
                query_embedding.tobytes(),
            )
        ).fetchall()
        return [dict(row) for row in results]

@app.get("/documents/")
async def list_documents():
    with get_db() as conn:
        results = conn.execute(
            """
            SELECT
                id,
                created_at,
                body,
                dek,
                hed,
                file_name,
                format,
                is_note
            FROM documents
            ORDER BY created_at DESC
            """
        ).fetchall()
        return [dict(row) for row in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)