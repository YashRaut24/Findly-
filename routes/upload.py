from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from core.chunker import chunk_text
from config import is_demo_cleared, mark_demo_cleared
from routes.search import retriever  # reuse the same retriever instance

router = APIRouter()


class TextUploadRequest(BaseModel):
    text: str


@router.post("/upload/text")
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


@router.post("/upload/file")
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