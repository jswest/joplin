SELECT load_extension('vector0');

CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  body TEXT,
  dek TEXT,
  hed TEXT,
  file_name TEXT,
  format TEXT, --e.g., `pdf` or `md`.
  is_note BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS chunks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  body TEXT,
  embedding VECTOR(384),
  document_id INTEGER NOT NULL,
  FOREIGN KEY(document_id) REFERENCES documents(id)
);

CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING vector(embedding);
CREATE INDEX IF NOT EXISTS chunks_document_id_idx ON chunks(document_id);