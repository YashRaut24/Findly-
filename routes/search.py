from fastapi import APIRouter
from pydantic import BaseModel

from core.retriever import Retriever
from core.generator import Generator
from core.resources import ResourceFinder

router = APIRouter()

retriever = Retriever()
generator = Generator()
resource_finder = ResourceFinder()

def load_documents(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

documents = load_documents("data/documents.txt")
retriever.add_documents(documents)


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def search(request: SearchRequest):
    query = request.query

    rewritten = generator.rewrite_query(query)

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
    answer = generator.generate(query, top_results)
    resources = resource_finder.get_external_resources(query)

    return {
        "query": query,
        "sources": top_results,
        "answer": answer,
        "resources": resources
    }