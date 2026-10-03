"""
Step 2 of the RAG pipeline: given a user question, return the most
relevant document chunks from the FAISS index built by ingest.py.
"""
import os
from typing import List, Dict
from dotenv import load_dotenv

from rag.embeddings import get_embedding_model
from rag.vector_store import FAISSVectorStore

load_dotenv()

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")


class Retriever:
    def __init__(self, vector_store_path: str = VECTOR_STORE_PATH):
        self.model = get_embedding_model()
        self.store = FAISSVectorStore.load(vector_store_path)

    def retrieve(self, query: str, k: int = 5, min_score: float = 0.0) -> List[Dict]:
        query_embedding = self.model.encode(query)[0]
        results = self.store.search(query_embedding, k=k)
        return [
            {**meta, "score": score}
            for meta, score in results
            if score >= min_score
        ]


_retriever_singleton = None


def get_retriever() -> Retriever:
    global _retriever_singleton
    if _retriever_singleton is None:
        _retriever_singleton = Retriever()
    return _retriever_singleton


if __name__ == "__main__":
    retriever = get_retriever()
    question = input("Ask your question: ")
    results = retriever.retrieve(question)

    if not results:
        print("\nSorry, I couldn't find relevant information in the available documents.")
    else:
        print("\nRelevant information:\n")
        for result in results:
            print("SCORE:", result["score"])
            print("SOURCE:", result["source"])
            print(result["text"])
            print("-" * 60)