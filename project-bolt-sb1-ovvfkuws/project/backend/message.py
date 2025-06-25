#!/usr/bin/env python3
import os
import json
import openai
import faiss
import numpy as np

# ─── CONFIG ────────────────────────────────────────────────────────
# 1) Put your key in .env or export OPENAI_API_KEY in your shell
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment")
openai.api_key = OPENAI_KEY

EMBED_MODEL = "text-embedding-ada-002"
CHAT_MODEL  = "gpt-3.5-turbo"
KNOWLEDGE_DIR = "knowledge"   # relative folder containing .txt docs
TOP_K = 3                     # how many docs to retrieve

# ─── HELPERS ───────────────────────────────────────────────────────
def load_documents(folder: str):
    docs = []
    for root, _, files in os.walk(folder):
        for fn in files:
            if fn.lower().endswith(".txt"):
                path = os.path.join(root, fn)
                with open(path, "r", encoding="utf-8") as f:
                    docs.append({"id": fn, "text": f.read()})
    if not docs:
        raise RuntimeError(f"No .txt files found under ./{folder}")
    return docs

def embed_texts(texts):
    """Batch-embed a list of strings via OpenAI embeddings"""
    resp = openai.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item["embedding"] for item in resp["data"]]

def build_faiss_index(embeddings):
    """Given a list of embeddings, build and return a FAISS index"""
    dim = len(embeddings[0])
    idx = faiss.IndexFlatL2(dim)
    array = np.array(embeddings, dtype="float32")
    idx.add(array)
    return idx

def retrieve(query: str, docs, idx, embeddings, k=TOP_K):
    """Return the top-k docs most similar to the query."""
    q_emb = embed_texts([query])[0]
    D, I = idx.search(np.array([q_emb], dtype="float32"), k)
    return [docs[i] for i in I[0]]

def chat_with_context(query: str, retrieved_docs):
    """Call OpenAI ChatCompletions with the retrieved snippets as context."""
    system_prompt = (
        "You are FIXR, an AI assistant specialized in tech support. "
        "Use the context below to answer the user's question as accurately as possible."
    )
    # Join the docs into one string, truncate if needed
    snippets = "\n\n".join(f"— {d['id']}:\n{d['text'][:500]}…" for d in retrieved_docs)
    messages = [
        {"role":"system", "content": system_prompt},
        {"role":"system", "content": f"Context documents:\n\n{snippets}"},
        {"role":"user",   "content": query}
    ]
    resp = openai.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=800,
        request_timeout=60
    )
    return resp.choices[0].message.content.strip()

# ─── MAIN LOOP ─────────────────────────────────────────────────────
def main():
    print("Loading knowledge documents…", end="", flush=True)
    docs = load_documents(KNOWLEDGE_DIR)
    print(f" found {len(docs)} docs.")
    
    print("Embedding documents…", end="", flush=True)
    embs = embed_texts([d["text"] for d in docs])
    idx  = build_faiss_index(embs)
    print(" done.")

    print("\nRAG Assistant is ready! Type your question (or 'exit'):\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in ("exit","quit"):
            break
        if not query:
            continue

        retrieved = retrieve(query, docs, idx, embs, k=TOP_K)
        print(f"\n→ Retrieved top {TOP_K} docs:", ", ".join(d["id"] for d in retrieved))

        answer = chat_with_context(query, retrieved)
        print("\nFIXR:", answer, "\n")

if __name__ == "__main__":
    main()
