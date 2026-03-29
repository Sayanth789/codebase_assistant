from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    texts = [c["content"] for c in chunks]

    vectors = model.encode(texts)

    return np.array(vectors).astype("float32")


def embed_query(query):
    vector = model.encode([query])

    return np.array(vector[0]).astype("float32")