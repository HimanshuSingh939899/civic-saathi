"""
A thin FAISS wrapper that persists both the index and the chunk metadata
(text + source file + category) needed to turn a matched vector back into
readable, attributable context.
"""
import os
import pickle
from typing import List, Dict, Tuple
import numpy as np
import faiss


class FAISSVectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata: List[Dict] = []

    def add(self, embeddings: np.ndarray, metadata: List[Dict]) -> None:
        assert embeddings.shape[0] == len(metadata), "embeddings/metadata length mismatch"
        self.index.add(embeddings.astype("float32"))
        self.metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, k: int = 4) -> List[Tuple[Dict, float]]:
        query_embedding = query_embedding.astype("float32").reshape(1, -1)
        scores, indices = self.index.search(query_embedding, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.metadata[idx], float(score)))
        return results

    def save(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "metadata.pkl"), "wb") as f:
            pickle.dump({"dimension": self.dimension, "metadata": self.metadata}, f)

    @classmethod
    def load(cls, path: str) -> "FAISSVectorStore":
        with open(os.path.join(path, "metadata.pkl"), "rb") as f:
            payload = pickle.load(f)
        store = cls(dimension=payload["dimension"])
        store.index = faiss.read_index(os.path.join(path, "index.faiss"))
        store.metadata = payload["metadata"]
        return store
