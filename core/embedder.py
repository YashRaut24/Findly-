from sentence_transformers import SentenceTransformer # converts text into numericals vectors(embeddings)
from config import EMBEDDING_MODEL # import embeddings model which converts text to vectors(embeddings)
class Embedder: # It creates embeddings, we will use to import this to other places where embeddings to be done
    def __init__(self): # runs automatically when class is called (constructor)
        self.model = SentenceTransformer(EMBEDDING_MODEL) # loads the model and then stored in self.model

    def embed(self, text: str) -> list: # accepts one text per input and returns embeddings as a python list
        return self.model.encode(text).tolist() # converts text into vector and stores into a list

    def embed_batch(self, texts: list) -> list: # accepts multiple texts  and returns embeddings of all
        return self.model.encode(texts).tolist() # converts many texts into vectors and returns a list

    
