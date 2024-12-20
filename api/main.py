from datetime import datetime
from fastapi import FastAPI, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from loguru import logger
from ollama import Client
from pathlib import Path
import tempfile
from typing import Optional
import shutil
from uuid import uuid4

from db import get_db
from .models import QueryRequest
from processing import process_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama = Client(host='http://localhost:11434')

@app.post("/documents/")
async def create_document(file: UploadFile):
    file_extension = file.filename.split('.')[-1]
    file_name = f"{str(uuid4())}.{file_extension}"
    file_path = f"./documents/{file_name}"
    logger.info(f"Processing new document with name '{file_name}'.")

    with open(f"./documents/{file_name}", "wb") as out_file:
        shutil.copyfileobj(file.file, out_file)
  
    try:
        full_text, chunks = process_document(f"./documents/{file_name}")
        logger.info(f"Chunked and extracted the document.")
        
        client = get_db()
        document_collection = client.get_or_create_collection("documents")
        chunk_collection = client.get_or_create_collection("chunks")

        hed_prompt = f"""
        Provide a very short title for this document. It should be no more than 100 characters in length. Only return the title text. Be concise!
        
        {chunks[0]}
        """
        hed = ollama.generate(
            model='mistral',
            prompt=hed_prompt,
            stream=False
        )
        logger.info(f"Received new hed: '{hed['response']}'")

        dek_prompt = f"""
        Provide a very short description for this document. It should be no more than one sentence in length. Only return the description text. Be concise!
        
        {chunks[0]}
        """
        dek = ollama.generate(
            model='mistral',
            prompt=dek_prompt,
            stream=False
        )
        logger.info(f"Received new dek: '{dek['response']}'")

        # Store the document
        document_id = str(uuid4())
        document_collection.add(
            documents=[full_text],
            metadatas=[{
                "created_at": datetime.utcnow().isoformat(),
                "dek": dek["response"],
                "file_name": file_name,
                "format": file_extension,
                "hed": hed["response"],
                "is_note": False,
            }],
            ids=[document_id]
        )
        logger.info(f"Document saved.'")
        
        # Store the chunks, referencing the document
        chunk_collection.add(
            documents=chunks,
            metadatas=[{
                "document_id": document_id,
                "chunk_index": i
            } for i in range(len(chunks))],
            ids=[f"{document_id}-chunk-{i}" for i in range(len(chunks))]
        )
        logger.info(f"Chunks saved.")
        
        return {"id": document_id, "chunks_processed": len(chunks)}
    except Exception as e:
        print(e)

@app.get('/documents/')
async def get_documents(semantic: Optional[str] = Query(None)):
    client = get_db()
    document_collection = client.get_or_create_collection("documents")
    chunk_collection = client.get_or_create_collection("chunks")
    if semantic:
        chunks_results = chunk_collection.query(
            query_texts=[semantic],
            n_results=20,
        )
        chunks_by_document_id = {}
        for i, chunk_meta in enumerate(chunks_results['metadatas'][0]):
            document_id = chunk_meta['document_id']
            chunk_body = chunks_results['documents'][0][i]
            if document_id not in chunks_by_document_id:
                document_result = document_collection.get(
                    ids=[document_id],
                    include=["metadatas"]
                )
                chunks_by_document_id[document_id] = {
                    'document_id': document_id,
                    'document_metadata': document_result['metadatas'][0],
                    'chunk_bodies': []
                }
            chunks_by_document_id[document_id]['chunk_bodies'].append(chunk_body)
        results = list(chunks_by_document_id.values())
    else:
        results = document_collection.get(
            include=["metadatas"]
        )
    return results

@app.post("/query/")
async def query_documents(request: QueryRequest):
    query = request.query
    try:
        client = get_db()
        document_collection = client.get_or_create_collection("documents")
        chunk_collection = client.get_or_create_collection("chunks")
        
        results = chunk_collection.query(
            query_texts=[query],
            n_results=5
        )
        
        context = "\n\n".join(results['documents'][0])
        
        # Create the prompt
        prompt = f"""
        Using only the following context, answer the query. Please be verbose."

        Context:
        {context}

        Query:
        {query}

        Answer:
        """

        response = ollama.generate(
            model='mistral',
            prompt=prompt,
            stream=False
        )

        chunks_by_document_id = {}
        for i, chunk_meta in enumerate(results['metadatas'][0]):
            document_id = chunk_meta['document_id']
            chunk_body = results['documents'][0][i]
            if document_id not in chunks_by_document_id:
                document_result = document_collection.get(
                    ids=[document_id],
                    include=["metadatas"]
                )
                chunks_by_document_id[document_id] = {
                    'document_id': document_id,
                    'document_metadata': document_result['metadatas'][0],
                    'chunk_bodies': []
                }
            chunks_by_document_id[document_id]['chunk_bodies'].append(chunk_body)
            
        return {
            "answer": response['response'],
            "documents": list(chunks_by_document_id.values())
        }
    except Exception as e:
        logger.error(e)

@app.get("/documents/{document_id}/pdf")
async def get_pdf(document_id: str):
    client = get_db()
    document_collection = client.get_or_create_collection("documents")
    
    result = document_collection.get(
        ids=[document_id],
        include=["metadatas"]
    )
    
    if not result['metadatas']:
        raise HTTPException(status_code=404, detail="Document not found")
        
    filename = result['metadatas'][0]['file_name']

    return FileResponse(
        f"./documents/{filename}",
        media_type='application/pdf',
        filename=filename
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)