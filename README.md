# JOPLIN

That's right, it's Ragtime!

——

### What is this thing?

`joplin` lets you upload a large number of documents and talk to them using a large-language model, but unlike other systems, this one should work entirely on your laptop computer. This means it's completely private, and your private documents, notes, and data can all stay, well, private. This kind of system is called retrieval-augmented generation, or RAG (hence the name Joplin).

### Core features

A local web front-end (powered by `SvelteKit`) where you can...

1. "Upload" a document (save it to a folder in the Joplin instance), name it, and associate metadata with it in a `SQLite` database managed by the API (see below).
2. Query into your documents using the back-end API (see below).

A local back-end API (powered by `FastAPI`) that will...

1. Clean, chunk, and embed each PDF or Markdown document using Huggingface's `sentence_transformers` library, and save each chunk to a `SQLite` database.
2. Take a plain-text query from the user, use `sentence_transformers` to embed it, get the relevent chunks using an ANN query into the `SQLite` database, and then pass those to `Mistral` to get generative text on top.

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

### TODOS

- Enable the ability to just query for similar notes (just semantic search).