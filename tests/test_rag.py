from backend.repo_loader import load_repo
from backend.chunker import chunk_code
from backend.embeddings import create_embeddings
from backend.vector_store import VectorStore
from backend.retriever import retrieve
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_rag_pipeline():
    files = load_repo("/home/user/Desktop/Python/AdvancedPython")
    print("FILES:", len(files))

    chunks = chunk_code(files)
    print("CHUNKS:", len(chunks))

    vectors = create_embeddings(chunks)
    print("EMBEDDINGS:", len(vectors))

    store = VectorStore(len(vectors[0]))
    store.add(vectors, chunks)

    results = retrieve("Where is authentication implemented?", store)
    print("RESULTS:", len(results))

    for r in results:
        print("File:", r["path"])
        print("Content snippet:", r["content"][:200], "\n")


if __name__ == "__main__":
    test_rag_pipeline()