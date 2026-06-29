import os # helps in interacting in operating system
from dotenv import load_dotenv # loads variables from .env file

load_dotenv() # reads the .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY") # stores the groq api key from .env to variable
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # model which will convert text into vectors(embeddings)
LLM_MODEL = "llama-3.1-8b-instant" # specifies llm for generating answers
CHROMA_PATH = "./chroma_findly" # path where chroma vector db will be stored
COLLECTION_NAME = "findly_kb" # name of collection (like table in db)
TOP_K_RESULTS = 5 # retrieve 5 most relevant document chunks from vector db
CHUNK_SIZE = 300 # split documents into 300 characters/tokens
CHUNK_OVERLAP = 30 # each chunk overlaps the previous one by 30 chunks as it helps in understanding the context of a line

