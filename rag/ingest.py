"""
Step 1 of the RAG pipeline: turn the .md/.txt files under data/document/
and the .json QA files under data/synthetic_data/ into a searchable
FAISS index.

Run this whenever you add or edit a document:
    python -m rag.ingest
"""
import os
from dotenv import load_dotenv

from utils.helpers import clean_text, chunk_text, list_source_files, load_synthetic_qa_files
from rag.embeddings import get_embedding_model
from rag.vector_store import FAISSVectorStore

load_dotenv()

DOCS_DIR = os.getenv("DOCS_DIR", "data/document")
SYNTHETIC_DIR = os.getenv("SYNTHETIC_DIR", "data/synthetic_data")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")


def load_and_chunk_documents(docs_dir: str = DOCS_DIR, synthetic_dir: str = SYNTHETIC_DIR):
    chunks, metadata = [], []

    # --- .md/.txt documents ---
    for filepath in list_source_files(docs_dir):
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
        text = clean_text(raw_text)

        category = os.path.basename(os.path.dirname(filepath))

        for i, chunk in enumerate(chunk_text(text)):
            chunks.append(chunk)
            metadata.append({
                "text": chunk,
                "source": filepath,
                "category": category,
                "chunk_id": i,
            })

    # --- synthetic QA-pair .json files ---
    for entry in load_synthetic_qa_files(synthetic_dir):
        chunk = f"Question: {entry.get('question', '')}\nAnswer: {entry.get('answer', '')}"
        chunks.append(chunk)
        metadata.append({
            "text": chunk,
            "source": entry["_source_file"],
            "category": entry.get("service", "unknown"),
            "chunk_id": entry.get("id", ""),
        })

    return chunks, metadata


def build_index():
    print(f"Scanning {DOCS_DIR} and {SYNTHETIC_DIR} for source documents...")
    chunks, metadata = load_and_chunk_documents()

    if not chunks:
        print("No documents found. Add .md/.txt files under data/document/ or .json files under data/synthetic_data/ first.")
        return

    n_files = len(set(m["source"] for m in metadata))
    print(f"Found {len(chunks)} chunks across {n_files} file(s). Embedding...")

    model = get_embedding_model()
    embeddings = model.encode(chunks)

    store = FAISSVectorStore(dimension=model.dimension)
    store.add(embeddings, metadata)
    store.save(VECTOR_STORE_PATH)

    print(f"Vector store saved to {VECTOR_STORE_PATH}/ ({len(chunks)} vectors, dim={model.dimension})")


if __name__ == "__main__":
    build_index()
