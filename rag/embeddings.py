"""
Wraps a local sentence-transformers model so the rest of the pipeline
never has to think about model loading, batching, or normalization.
"""
import os
from functools import lru_cache
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


class EmbeddingModel:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Return L2-normalized embeddings, shape (len(texts), dim)."""
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()


@lru_cache(maxsize=1)
def get_embedding_model() -> EmbeddingModel:
    """Load the embedding model once per process and reuse it everywhere."""
    return EmbeddingModel()
