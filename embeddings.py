from sentence_transformers import SentenceTransformer
import numpy as np

# Load a free embedding model (downloads once, ~90MB)
model = SentenceTransformer("all-MiniLM-L6-v2")

# ─── Part 1: Basic Embedding ───────────────────────────────────────
text = "How do I fix a memory leak in Python?"
vector = model.encode(text)

print(f"Text: {text}")
print(f"Vector dimensions: {len(vector)}")
print(f"First 5 values: {vector[:5]}")

# ─── Part 2: Similarity Comparison ─────────────────────────────────
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot_product / magnitude

sentences = [
    "How do I fix a memory leak in Python?",   # query
    "Python garbage collection and memory management",  # similar
    "Tips for managing RAM overflow in applications",   # similar
    "How to bake chocolate chip cookies",               # unrelated
    "Best restaurants in Mumbai",                       # unrelated
]

query = sentences[0]
query_vector = model.encode(query)

print(f"\nQuery: '{query}'\n")
print("Similarity scores:")

for sentence in sentences[1:]:
    vector = model.encode(sentence)
    score = cosine_similarity(query_vector, vector)
    print(f"  {score:.4f} → '{sentence}'")

# ─── Part 3: Mini Semantic Search ──────────────────────────────────
print("\n─── Semantic Search Demo ───")

documents = [
    "Python memory leaks occur when objects are not garbage collected",
    "React hooks allow functional components to use state",
    "Heap overflow happens when too much memory is allocated",
    "MongoDB uses documents instead of tables for storage",
    "Memory profilers help identify which objects consume RAM",
    "Docker containers isolate application environments",
    "Python garbage collection automatically frees unreachable objects",
    "Reference cycles in Python can sometimes increase memory usage",
    "Photosynthesis converts sunlight into chemical energy in plants",
]

doc_vectors = model.encode(documents)

def semantic_search(query, documents, doc_vectors, top_k=3):
    query_vector = model.encode(query)
    scores = [cosine_similarity(query_vector, dv) for dv in doc_vectors]
    ranked = sorted(zip(scores, documents), reverse=True)
    return ranked[:top_k]

user_query = "how to find memory problems in Python"
results = semantic_search(user_query, documents, doc_vectors)

print(f"Query: '{user_query}'")
print("\nTop results:")
for score, doc in results:
    print(f"  [{score:.4f}] {doc}")