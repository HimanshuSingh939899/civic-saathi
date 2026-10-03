import os
import re
import json
from typing import List


def clean_text(text: str) -> str:
    """
    Clean unnecessary whitespace from document text.
    """
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> List[str]:
    """
    Split text into overlapping chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_length:
            break
        start = end - chunk_overlap

    return chunks


def list_source_files(docs_dir: str) -> List[str]:
    """
    Find all .md and .txt files inside data/documents/.
    """
    source_files = []
    for root, _, files in os.walk(docs_dir):
        for filename in files:
            if filename.lower().endswith((".md", ".txt")):
                filepath = os.path.join(root, filename)
                source_files.append(filepath)
    return sorted(source_files)


def extract_section(markdown_text: str, section_title: str) -> str:
    """
    Pull just one '### <section_title>' section out of the LLM's
    structured markdown response, e.g. "Steps", "Required Documents".
    Returns "" if that section isn't present in the response.
    """
    pattern = rf"###\s*{re.escape(section_title)}\s*\n(.*?)(?=\n###|\Z)"
    match = re.search(pattern, markdown_text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def load_synthetic_qa_files(synthetic_dir: str) -> List[dict]:
    """
    Reads every .json file in data/synthetic_data/.
    Each line looks like: // {"question": ..., "answer": ...}
    We strip the leading "//" so it becomes valid JSON, then parse it.
    """
    qa_entries = []

    if not os.path.isdir(synthetic_dir):
        return qa_entries

    for filename in os.listdir(synthetic_dir):
        if not filename.lower().endswith(".json"):
            continue

        filepath = os.path.join(synthetic_dir, filename)
        service_name = os.path.splitext(filename)[0]

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("//"):
                    line = line[2:].strip()
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                entry["service"] = service_name
                entry["_source_file"] = filepath
                qa_entries.append(entry)

    return qa_entries
