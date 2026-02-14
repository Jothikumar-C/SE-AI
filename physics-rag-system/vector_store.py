"""
Vector Store using FAISS
Persistent single index stored on disk
"""

import faiss
import numpy as np
import os
import pickle
from config import VECTOR_STORE_PATH

DIMENSION = 1536  # text-embedding-3-small dimension


class VectorStore:

    def __init__(self):
        self.index = faiss.IndexFlatL2(DIMENSION)
        self.documents = []

    def add(self, embeddings, docs):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.documents.extend(docs)

    def save(self):
        faiss.write_index(self.index, VECTOR_STORE_PATH)
        with open(VECTOR_STORE_PATH + ".pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def load(self):
        if os.path.exists(VECTOR_STORE_PATH):
            self.index = faiss.read_index(VECTOR_STORE_PATH)
            with open(VECTOR_STORE_PATH + ".pkl", "rb") as f:
                self.documents = pickle.load(f)

    def search(self, query_embedding, k=4):
        vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(vector, k)

        results = []
        for idx in indices[0]:
            results.append(self.documents[idx])

        return results
