import sys
import os
import tempfile
from git import Repo

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from backend.llm import ask_llm
from backend.retriever import retrieve
from backend.vector_store import VectorStore
from backend.embeddings import create_embeddings
from backend.chunker import chunk_code
from backend.repo_loader import load_repo


def load_repo_from_url(repo_url):
    """Load repository from local path or clone from Git URL."""

    if os.path.isdir(repo_url):
        print(f"Using local directory: {repo_url}")
        return repo_url

    try:
        temp_dir = tempfile.mkdtemp()
        print(f"Cloning remote repo: {repo_url} into {temp_dir}")
        Repo.clone_from(repo_url, temp_dir)
        return temp_dir
    except Exception as e:
        raise gr.Error(f"Failed to load repository: {str(e)}")


def answer_query(repo_url, question):
    try:
        repo_path = load_repo_from_url(repo_url)

        files = load_repo(repo_path)

        if not files:
            return "No code files found in the repository."

        chunks = chunk_code(files)

        if not chunks:
            return "No code chunks could be generated from the repository."


        repo_name = os.path.basename(os.path.normpath(repo_path))
        index_path = f"{repo_name}_index.faiss"

        store = VectorStore(384, index_file=index_path)
        # but why 384? Because the embedding size of  all-MiniLM-L6-v2 is 384 dimensions. 

        if store.index.ntotal == 0:
            print("Building embeddings and index...")

            vectors = create_embeddings(chunks)
            store.add(vectors, chunks)

        else:
            print("Using existing FAISS index")

        results = retrieve(question, store, top_k=3)

        if not results:
            return "No relevant code found."

        context = "\n\n".join([r["content"][:800] for r in results])
        answer = ask_llm(context, question)


        return answer

    except Exception as e:
        return f"Error processing request: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("# Codebase Assistant 🔍")

    repo_input = gr.Textbox(
        label="Repository path or Git URL",
        placeholder="/home/user/project or https://github.com/user/repo.git"
    )

    question_input = gr.Textbox(label="Ask a question about the code")

    output = gr.Textbox(label="Result", lines=15)

    ask_button = gr.Button("Ask")

    ask_button.click(
        fn=answer_query,
        inputs=[repo_input, question_input],
        outputs=output
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)