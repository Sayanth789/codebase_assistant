# 🧠 Codebase Assistant 🔍

Welcome to **Codebase Assistant**, your AI-powered tool to explore and understand code repositories effortlessly! This project lets you ask natural language questions about any codebase and get relevant answers instantly. Perfect for developers, students, or anyone diving into unfamiliar projects.

---

## 🚀 Features

- **Query any code repository**  
  Ask questions about your project’s code using plain English. Supports both local directories and GitHub URLs.

- **AI-powered answers**  
  Uses LLaMA (or your chosen LLM) to generate clear, concise explanations from your code.

- **Smart code indexing with FAISS**  
  Generates embeddings and builds an index for fast retrieval of relevant code snippets.

- **Caching for speed**  
  Once a repo is indexed, queries become faster using the existing FAISS index.

- **Extensible backend**  
  Easily swap embeddings, chunking, or LLM models as needed.

---

## 🛠️ Installation

1. Clone the repository:  
```bash
git clone https://github.com/your-username/codebase-assistant.git
cd codebase-assistant
```
## Install dependencies (recommended in a virtual environment):
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the app: 
```python ui/app.py```
Go to ```http://localhost/7860```

## Usage 🗒️ 📝 

* Enter a local repo path or a GitHub repo URL.
* Type your question about the code.
* Click Ask to get an AI-generated answer!

Example Questions:

> "Explain the function of process_data in this repo."
> "What are the main classes in this project?"
> "How does the login system work?"

# 📂Project Structure
```
├── backend
│   ├── app.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── __init__.py
│   ├── llm.py
│   ├── parser.py
│   ├── repo_loader.py
│   ├── retriever.py
│   └── vector_store.py
├── data
├── Dockerfile
├── frontend
├── requirements.txt
├── scripts
│   └── run_rag_test.py
├── tests
│   └── test_rag.py
├── Try
└── ui
    ├── app.py
    └── static
```
    
