from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Document(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    body: str
    dek: Optional[str] = None
    hed: Optional[str] = None
    file_name: str
    format: str
    is_note: bool = False

class Query(BaseModel):
    text: str
    limit: int = 10

class QueryRequest(BaseModel):
    query: str