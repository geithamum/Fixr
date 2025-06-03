# Web Search RAG Assistant

A command-line tool that searches the web for information and generates solutions using OpenAI's GPT model with RAG (Retrieval-Augmented Generation).

## Features

- Web search using SerpAPI
- Text extraction from web pages
- Vector storage using FAISS
- RAG-based solution generation using OpenAI's GPT model
- Comprehensive error handling and logging

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export SERPAPI_KEY="your-serpapi-key"
```

## Usage

Ask a question:
```bash
python main.py ask "How do I implement authentication in FastAPI?"
```

The tool will:
1. Search the web for relevant information
2. Extract and process the content
3. Build a vector store for semantic search
4. Retrieve the most relevant chunks
5. Generate a detailed solution using GPT-4

## Configuration

You can modify the following settings in `config.py`:
- `MAX_SEARCH_RESULTS`: Number of search results to process (default: 5)
- `CHUNK_SIZE`: Size of text chunks for vector store (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K_CHUNKS`: Number of chunks to retrieve (default: 5)
- `MODEL_NAME`: OpenAI model to use (default: "gpt-4") 