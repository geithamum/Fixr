import typer
from search import search_and_extract
from rag_pipeline import build_vector_store, retrieve_chunks
from generate import generate_solution

app = typer.Typer()

@app.command()
def ask(question: str):
    print("🔍 Searching the web...")
    documents = search_and_extract(question)

    print("🧠 Building vector store...")
    vector_store = build_vector_store(documents)

    print("📥 Retrieving relevant chunks...")
    top_chunks = retrieve_chunks(vector_store, question)

    print("💡 Generating solution...")
    answer = generate_solution(question, top_chunks)

    print("\n✅ Solution:\n", answer)

if __name__ == "__main__":
    app()
