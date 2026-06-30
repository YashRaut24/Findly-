from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import search, upload

app = FastAPI(title="Findly API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router)
app.include_router(upload.router)


@app.get("/")
def root():
    return {"message": "Findly API is running"}