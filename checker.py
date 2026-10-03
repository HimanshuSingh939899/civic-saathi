"""
checker.py

Background job: every 24 hours, poll official government notification
pages for each service, detect NEW notifications, and automatically
ingest them into the RAG knowledge base (chunk -> embed -> add to
FAISS index) so the system stays up to date without manual re-ingestion.

Assumes the existing project structure:
    data/document/<service>/*.md         -> per-service source docs
    data/vector_store/                    -> FAISS index + metadata
    rag/embeddings.py    -> get_embedder() / embedder.embed(text)
    rag/vector_store.py  -> VectorStore.add(vectors, metadata), .save()
    utils/helpers.py     -> clean_text(text), chunk_text(text)

Adjust NOTIFICATION_SOURCES and the ingest_* calls below to match
your actual module APIs if they differ.
"""

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from utils.helpers import clean_text, chunk_text
from rag.embeddings import get_embedder
from rag.vector_store import VectorStore

# ---------------------------------------------------------------------
# CONFIG — fill in the real notification/circular pages for each service
# ---------------------------------------------------------------------
NOTIFICATION_SOURCES = {
    "aadhar": "https://uidai.gov.in/en/notifications.html",
    "pan": "https://www.incometax.gov.in/iec/foportal/latest-updates",
    "income": "https://example.gov.in/income-certificate/notifications",
    "pm_kisan": "https://pmkisan.gov.in/Documents/Notifications.aspx",
    "ayushman": "https://pmjay.gov.in/press-release",
}

SEEN_FILE = Path("data/seen_notifications.json")
DOCS_ROOT = Path("data/document")
CHECK_INTERVAL_SECONDS = 24 * 60 * 60  # 24 hours


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def load_seen() -> dict:
    if SEEN_FILE.exists():
        return json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    return {}


def save_seen(seen: dict) -> None:
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(seen, indent=2), encoding="utf-8")


def fetch_page_text(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Strip scripts/styles, keep visible text only
    for tag in soup(["script", "style"]):
        tag.decompose()
    return clean_text(soup.get_text(separator="\n"))


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def save_notification_as_doc(service: str, text: str) -> Path:
    """Save the new notification text as a .md file in the service's
    document folder, same convention as your existing curated docs."""
    service_dir = DOCS_ROOT / service
    service_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = service_dir / f"notification_{timestamp}.md"
    out_path.write_text(text, encoding="utf-8")
    return out_path


def ingest_new_doc(service: str, doc_path: Path, embedder, store: VectorStore) -> int:
    """Chunk the new doc and add it to the FAISS vector store."""
    text = doc_path.read_text(encoding="utf-8")
    chunks = chunk_text(text, chunk_size=1000, overlap=150)

    vectors = [embedder.embed(chunk) for chunk in chunks]
    metadata = [
        {"service": service, "source": str(doc_path), "chunk_index": i, "text": chunk}
        for i, chunk in enumerate(chunks)
    ]

    store.add(vectors, metadata)
    return len(chunks)


# ---------------------------------------------------------------------
# Main check routine
# ---------------------------------------------------------------------
def run_check() -> None:
    print(f"[{datetime.utcnow().isoformat()}] Checking for new notifications...")

    seen = load_seen()
    embedder = get_embedder()
    store = VectorStore.load()  # adjust if your loader has a different name

    any_updates = False

    for service, url in NOTIFICATION_SOURCES.items():
        try:
            text = fetch_page_text(url)
        except Exception as e:
            print(f"  [!] Failed to fetch {service} ({url}): {e}")
            continue

        h = content_hash(text)

        if seen.get(service) == h:
            print(f"  - {service}: no change")
            continue

        print(f"  + {service}: new/changed content detected, updating RAG index")
        doc_path = save_notification_as_doc(service, text)
        n_chunks = ingest_new_doc(service, doc_path, embedder, store)
        print(f"    added {n_chunks} chunks from {doc_path.name}")

        seen[service] = h
        any_updates = True

    if any_updates:
        store.save()
        save_seen(seen)
        print("Vector store updated and saved.")
    else:
        print("No updates this cycle.")


# ---------------------------------------------------------------------
# Scheduler loop (simple; swap for a real cron job / systemd timer in prod)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        run_check()
        print(f"Sleeping for 24 hours...\n")
        time.sleep(CHECK_INTERVAL_SECONDS)