# JOPLIN

That's right, it's Ragtime!

——

### What is this thing?

`joplin` lets you upload a large number of documents and talk to them using a large-language model, but unlike other systems, this one should work entirely on your laptop computer. This means it's completely private, and your private documents, notes, and data can all stay, well, private. This kind of system is called retrieval-augmented generation, or RAG (hence the name Joplin).

### Future features

1. The ability to create Markdown notes in the front-end and save them into the database as if they were new documents.
2. The ability to select which source documents or type of source documents you want to include in your RAG task.


### Installation

Install `ollama` (instructions [here](https://ollama.com/download)).

Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

npm install

ollama pull mistral

python db/connection.py
```

### Running it

Make sure that `ollama` is running.

This will open up an Electron app:

```bash
NODE_ENV=development npm run dev
```

To run in total development mode:

```bash
source .venv/bin/activate
npm run chroma
```

```bash
source .venv/bin/activate
npm run server
```

```bash
npm run vite
```

### The Zotero connection

Try:

```bash
source .venv/bin/activate
playwright install
python scripts/convert-zotero-to-pdf.py path/to/zotero/export path/to/output/dir
```

### TODOS

- Enable the ability to just query for similar notes (just semantic search).