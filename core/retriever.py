import chromadb # imports chroma vector database
from config import CHROMA_PATH, COLLECTION_NAME, TOP_K_RESULTS # imports necessary requirements for chroma vector db
from core.embedder import Embedder # imports embedder class to perform text to vector conversion 

class Retriever: # it , we will use to store and retrieve relevant documents
    def __init__(self):
        self.embedder = Embedder() # loads embedder model
        self.client = chromadb.PersistentClient(path=CHROMA_PATH) # defines and connects the path for the vector to get stored
        self.collection = self.client.get_or_create_collection(  # get or create the collections name and the req for the vector
            name=COLLECTION_NAME, # defines name for collection
            metadata={"hnsw:space": "cosine"} #configures graph based algorithm with cosine similarity to ,easure 
        )
        
    def add_documents(self, documents: list[str]): # add documents given by user one by one
        existing = self.collection.count() # Counts the documents which are present
        if existing > 0: # checks if collection already contains documents
            print(f"Collection already has {existing} documents, skipping ingestion") # Restrict overlapping or adding another collections
            return     

        embeddings = self.embedder.embed_batch(documents) # Converts all documents into embeddings
        self.collection.add(  # adds the collection specifying the documents by their id's 
            ids = [f"doc_{i}" for i in range(len(documents))], # creates unique id for each document
            embeddings=embeddings,  # stores the generated embeddings 
            documents=documents # stores original text along with embeddings
        )
        print(f"Ingested {len(documents)} documents into vector DB") 


    def retrieve(self, query: str, k: int = TOP_K_RESULTS) -> list[str]: # retrieves or take back the top 5 results from the documents and query is user input
        query_embedding = self.embedder.embed(query) # converts users ques into embeddings
        results = self.collection.query(  # returns results of the top 5 tests
            query_embeddings=[query_embedding],
            n_results=k
        )

        return results["documents"][0] # Since >0 document isnt accpeteable it will only return document at 0th index