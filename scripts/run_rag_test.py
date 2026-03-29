from backend.retriever import retrieve
from backend.vector_store import VectorStore
from backend.embeddings import create_embeddings
from backend.chunker import chunk_code
import os

# Path to your local code file or folder
file_path = os.path.expanduser("~/Desktop/Python/BPE/fib.py")

# Read file and chunk
with open(file_path, "r") as f:
    chunks = chunk_code([{"path": file_path, "content": f.read()}], chunk_size=50)
# Create embeddings
vectors = create_embeddings(chunks)

# Initialize vector store
store = VectorStore(len(vectors[0]))
store.add(vectors, chunks)

# Query the code
results = retrieve("Compute Fibonacci sequence", store)

# Print top results
for r in results:
    print("File:", r["path"])
    print("Code snippet:", r["content"][:200], "...\n")