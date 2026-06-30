from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from core.retriever import Retriever
from core.generator import Generator
from core.resources import ResourceFinder
from core.chunker import chunk_text
from config import is_demo_cleared, mark_demo_cleared

app = FastAPI(title="Findly API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class TextUploadRequest(BaseModel):
    text: str

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
    resources = resource_finder.get_external_resources(query)

    return {
        "query": query,
        "sources": top_results,
        "answer": answer,
        "resources": resources
    }

# ─── NEW: Upload pasted text ──────────────────────────────────
@app.post("/upload/text")
def upload_text(request: TextUploadRequest):
    chunks = chunk_text(request.text)

    is_first = not is_demo_cleared()
    retriever.add_user_documents(chunks, is_first_upload=is_first)
    if is_first:
        mark_demo_cleared()

    return {
        "message": f"Added {len(chunks)} chunks to knowledge base",
        "total_documents": retriever.collection.count()
    }

# ─── NEW: Upload .txt/.md file ────────────────────────────────
@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    if not (file.filename.endswith(".txt") or file.filename.endswith(".md")):
        return {"error": "Only .txt and .md files are supported"}

    content = await file.read()
    text = content.decode("utf-8")
    chunks = chunk_text(text)

    is_first = not is_demo_cleared()
    retriever.add_user_documents(chunks, is_first_upload=is_first)
    if is_first:
        mark_demo_cleared()

    return {
        "message": f"Added {len(chunks)} chunks from {file.filename}",
        "total_documents": retriever.collection.count()
    }