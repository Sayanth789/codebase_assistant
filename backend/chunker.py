# backend/chunker.py

def chunk_code(files, chunk_size=100, overlap=20):
    """
    Split code files into chunks for RAG retrieval.

    Args:
        files (list): List of pathlib.Path objects pointing to code files
        chunk_size (int): Number of lines per chunk
        overlap (int): Number of lines to overlap between chunks

    Returns:
        list: List of chunks with file path and content
    """
    all_chunks = []

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
            continue

        lines = content.split("\n")
        start = 0
        while start < len(lines):
            end = min(start + chunk_size, len(lines))
            chunk_text = "\n".join(lines[start:end])
            all_chunks.append({"path": str(file_path), "content": chunk_text})
            if end == len(lines):
                break
            start += chunk_size - overlap  # move forward with overlap

    return all_chunks