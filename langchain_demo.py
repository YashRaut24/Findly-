import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

load_dotenv()

llm = ChatGroq(model = "llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print (" === Basic LLM Chain ===\n")

prompt = ChatPromptTemplate.from_template("Answer this question in 2 sentences: {question}")

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"question" : "What is a vector database?"})
print(f"Response: {response}\n")


large_text = """
Python is a high-level programming language known for its simplicity.
It is widely used in web development, data science, and AI engineering.
Python's garbage collector automatically manages memory by tracking object references.
When objects are no longer referenced, they become eligible for garbage collection.
Reference cycles occur when two objects reference each other, potentially causing memory leaks.
The gc module in Python provides tools to detect and fix reference cycles.
Memory profilers like memory_profiler and tracemalloc help identify memory usage.

LangChain is a framework for building LLM-powered applications.
It provides components for document loading, text splitting, and vector storage.
The framework supports multiple LLM providers including OpenAI, Anthropic, and Groq.
LangChain's retrieval system makes it easy to build RAG applications.
LCEL allows chaining components together using the pipe operator.

Vector databases store embeddings for efficient similarity search.
Chroma is a popular open-source vector database for local development.
Pinecone and Weaviate are cloud-based alternatives for production use.
HNSW indexing allows vector databases to search millions of vectors quickly.
"""

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

docs = [Document(page_content=large_text)]
chunks = splitter.split_documents(docs)

print(f"Original text length: {len(large_text)} characters")
print(f"Split into {len(chunks)} chunks")
print(f"\nFirst chunk:\n'{chunks[0].page_content}'\n")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="langchain_demo"
)

retriever = vectorstore.as_retriever(search_kwargs={"k":3})

rag_prompt = ChatPromptTemplate.from_template("""
Answer the question using only the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

questions = [
    "How does Python handle memory management?",
    "What is LCEL in LangChain?",
    "What is the capital of France?", 
    "Suppose you are building a memory-efficient Retrieval-Augmented Generation (RAG) application using Python and LangChain, where millions of document embeddings are stored in a vector database. Explain how Python's garbage collection system, memory profiling tools, LangChain's retrieval pipeline, and HNSW indexing in vector databases work together to ensure efficient memory usage and fast retrieval performance."
]

for question in questions:
    print(f"Q: {question}")
    answer = rag_chain.invoke(question)
    print(f"A: {answer}\n")