# This module is our "memory bank" for document chunks.
# It uses FAISS to quickly find the most relevant pieces of text for any question.
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        """
        Set up a new vector store with a given embedding size.
        Think of this as creating a blank notebook for storing all our document pieces!
        """
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add_embeddings(self, embeddings, chunks):
        """
        Add new embeddings and their corresponding text chunks to our memory bank.
        """
        self.index.add(np.array(embeddings))
        self.chunks.extend(chunks)

    def search(self, query_embedding, top_k=3):
        """
        Find the top_k most similar chunks to the query embedding.
        This is like asking, "Which parts of my notes are most relevant to this question?"
        """
        D, I = self.index.search(np.array([query_embedding]), top_k)
        return [self.chunks[i] for i in I[0]]
