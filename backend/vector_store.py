import faiss
import numpy as np
import pickle
import os


class VectorStore:
    def __init__(self, dim, index_file=None):
        self.dim = dim
        self.index_file = index_file
        self.chunks = []

        if index_file and os.path.exists(index_file):
            self.load_index()
        else:
            self.index = faiss.IndexFlatL2(dim)

    def add(self, vectors, chunks):
        vectors = np.array(vectors).astype("float32")

        if self.index.ntotal == 0:
            self.index.add(vectors)
            self.chunks.extend(chunks)

        if self.index_file:
            self.save_index()

            
    def search(self, query_vector, top_k=3):
        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i in indices[0]:
            if i < len(self.chunks):
                results.append(self.chunks[i])

        return results

    def save_index(self):
        faiss.write_index(self.index, self.index_file)

        with open(self.index_file + ".meta", "wb") as f:
            pickle.dump(self.chunks, f)

    def load_index(self):
        self.index = faiss.read_index(self.index_file)

        meta_file = self.index_file + ".meta"

        if os.path.exists(meta_file):
            with open(meta_file, "rb") as f:
                self.chunks = pickle.load(f)
        else:
            self.chunks = []