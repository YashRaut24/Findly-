def chunk_text(text: str, chunk_size: int = 300, overlap: int = 30) -> list[str]:
    """Simple sliding-window chunker — splits text into overlapping pieces."""
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks