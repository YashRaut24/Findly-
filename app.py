from core.retriever import Retriever
from core.generator import Generator

def load_documents(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def search(query: str, retriever: Retriever, generator: Generator) -> dict:
    print(f"\nQuery: '{query}'")

    rewritten = generator.rewrite_query(query)
    print(f"Rewritten queries: {rewritten}")

    all_results = []
    for q in [query] + rewritten:
        results = retriever.retrieve(q, k=3)
        all_results.extend(results)

    seen = set()
    unique_results = []
    for doc in all_results:
        if doc not in seen:
            seen.add(doc)
            unique_results.append(doc)

    top_results = unique_results[:5]
    print(f"Retrieved {len(top_results)} unique chunks")

    answer = generator.generate(query, top_results)

    return {
        "query": query,
        "sources": top_results,
        "answer": answer
    }

def main():
    retriever = Retriever()
    generator = Generator()

    documents = load_documents("data/documents.txt")
    retriever.add_documents(documents)

    print("\n" + "="*50)
    print("FINDLY — Intelligent Search")
    print("="*50)

    test_queries = [
        "how does Python handle memory?",
        "what is RAG and how does it work?",
        "how do vector databases search efficiently?",
    ]

    for query in test_queries:
        result = search(query, retriever, generator)
        print(f"\nANSWER: {result['answer']}")
        print("-"*40)

if __name__ == "__main__":
    main()