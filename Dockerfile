FROM python:3.10-slim

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r requirements.txt

# Pre-download the sentence-transformers model
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Copy your app and backend folder
COPY . .

# Create uploads folder inside the container (for local repo queries)
RUN mkdir -p /app/uploads

# Set Python path
ENV PYTHONPATH=/app

# Expose Gradio port
EXPOSE 7860

# Run your main UI app
CMD ["python3", "ui/app.py"]