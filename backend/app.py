import sys
import os
import tempfile
import shutil
import pathlib

# Ensure the backend modules are in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from backend.retriever import retrieve
from backend.vector_store import VectorStore
from backend.embeddings import create_embeddings
from backend.chunker import chunk_code
from backend.repo_loader import load_repo

def answer_query(repo_input, question):
    """
    Handles both Git URLs and local Docker volume paths.
    """
    source = repo_input.strip()
    
    if not source or not question:
        return "Please enter both the repository source and a question."

    try:
        # 1. Check if the input is the local mounted directory (/app/uploads)
        if os.path.isdir(source):
            print(f"Directory detected: {source}. Skipping git clone.")
            # Pass the local path directly to your loader
            files = load_repo(source)
            
        # 2. If it's not a local directory, check if it's a URL
        elif source.startswith("http://") or source.startswith("https://"):
            print(f"URL detected: {source}. Attempting to clone...")
            files = load_repo(source)
            
        else:
            return f"Error: '{source}' is not a valid directory or Git URL."

        # --- Logic Pipeline ---
        chunks = chunk_code(files)
        if not chunks:
            return "No supported code files found. Please check your folder/repo."

        vectors = create_embeddings(chunks)
        
        # Initialize VectorStore
        store = VectorStore(len(vectors[0]))
        store.add(vectors, chunks)
        
        # Get results
        results = retrieve(question, store, top_k=3)

        if not results:
            return "No relevant code snippets found."

        formatted_results = []
        for r in results:
            res = f"--- File: {r['path']} ---\n{r['content'][:500]}..."
            formatted_results.append(res)

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Error: {str(e)}"

# --- UI Interface ---
with gr.Blocks(title="AI Codebase Assistant") as demo:
    gr.Markdown("# 🤖 AI Codebase Assistant")
    
    with gr.Row():
        with gr.Column():
            repo_input = gr.Textbox(
                label="Repo URL or Local Path", 
                placeholder="/app/uploads",
                value="/app/uploads" # Default to your mount path
            )
            question_input = gr.Textbox(label="Question", placeholder="What does this code do?")
            btn = gr.Button("Run Analysis", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(label="Answer", lines=15)

    btn.click(fn=answer_query, inputs=[repo_input, question_input], outputs=output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, block=True)