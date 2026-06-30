from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # helps frontend to send req to backend
from pydantic import BaseModel # defines the structure of req data and automatically validate it

from core.retriever import Retriever
from core.generator import Generator

app = FastAPI(title="Findly API")


app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["*"], allow_headers=["*"],)

#inititalize once server starts not everytime
retriever = Retriever()
generator = Generator()

def load_documents(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]
    

documents = load_documents("data/documents.txt")
retriever.add_documents(documents)

class SearchRequest(BaseModel):
    query: str

@app.get("/")
def root(): 
    return {"message": "Findly API is running"}

@app.post("/search")
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

    return {
        "query": query,
        "sources": top_results,
        "answer": answer
    }
