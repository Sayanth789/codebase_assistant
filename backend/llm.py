import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

def ask_llm(context, question):

    prompt = f"""
You are an AI code assistant.

Context from the repository:
{context}

Question:
{question}

Explain clearly.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]