import numpy as np
from sentence_transformers import SentenceTransformer
from backend.embeddings import embed_query



def retrieve(query, store, top_k=3):
    query_vector = embed_query(query)
    results = store.search(query_vector, top_k)
    return results