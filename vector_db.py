import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

# ─── Setup ─────────────────────────────────────────────────────────
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Create a persistent Chroma client — saves to disk
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or get a collection
collection = chroma_client.get_or_create_collection(
    name="findly_documents",
    metadata={"hnsw:space": "cosine"}  # use cosine similarity
)

# ─── Part 1: Add Documents ─────────────────────────────────────────
documents = [
    "Python memory leaks occur when objects are not garbage collected",
    "React hooks allow functional components to use state and lifecycle",
    "Heap overflow happens when too much memory is allocated on the stack",
    "MongoDB uses documents instead of tables for flexible storage",
    "Memory profilers help identify which objects consume the most RAM",
    "Docker containers isolate application environments for deployment",
    "Python garbage collection automatically frees unreachable objects",
    "Reference cycles in Python can cause unexpected memory retention",
    "Webpack bundles JavaScript modules for browser consumption",
    "Redis is an in-memory data store used for caching and sessions",
]

# Generate embeddings for all documents
embeddings = embedding_model.encode(documents).tolist()

# Add to vector database
collection.add(
    ids=[f"doc_{i}" for i in range(len(documents))],
    embeddings=embeddings,
    documents=documents,
    metadatas=[{"index": i} for i in range(len(documents))]
)

print(f"Added {collection.count()} documents to vector database\n")

# ─── Part 2: Semantic Search ───────────────────────────────────────
def search(query: str, n_results: int = 3):
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results["documents"][0], results["distances"][0]

print("=== Semantic Search ===\n")
queries = [
    "how to fix memory problems in Python",
    "frontend JavaScript tooling",
    "database storage options",
]

for query in queries:
    docs, distances = search(query)
    print(f"Query: '{query}'")
    for doc, dist in zip(docs, distances):
        print(f"  [{1-dist:.4f}] {doc}")
    print()

# ─── Part 3: RAG Preview ───────────────────────────────────────────
print("=== RAG Preview ===\n")

def answer_with_context(question: str):
    # Step 1 — retrieve relevant documents
    docs, _ = search(question, n_results=3)
    context = "\n".join(docs)

    # Step 2 — generate answer using retrieved context
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"Answer the question using only this context:\n{context}"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=150
    )
    return response.choices[0].message.content, docs

question = "What causes memory issues in Python and how can I find them?"
answer, sources = answer_with_context(question)

print(f"Question: {question}")
print(f"\nSources used:")
for doc in sources:
    print(f"  • {doc}")
print(f"\nAnswer: {answer}")