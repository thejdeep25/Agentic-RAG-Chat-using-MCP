
from utils.chunking import chunk_text
from embeddings.embedder import get_embeddings

# This agent is in charge of taking in new documents, breaking them up, and storing them for later.
# Think of it as the librarian who catalogs every new book!
class IngestionAgent:
    def __init__(self, dispatcher, vector_store, parsers):
        """
        Set up the IngestionAgent with everything it needs to process documents.
        It registers itself so it can be called when a new file arrives.
        """
        self.dispatcher = dispatcher
        self.vector_store = vector_store
        self.parsers = parsers
        dispatcher.register_agent("IngestionAgent", self.handle)

    def handle(self, message):
        """
        When a new document arrives, this method:
        1. Figures out what type of file it is
        2. Reads and parses the file
        3. Breaks the text into chunks
        4. Gets embeddings for each chunk
        5. Stores everything in the vector store for future searching
        """
        file_path = message.payload["file_path"]
        file_type = message.payload["file_type"]
        text = self.parsers[file_type](file_path)
        chunks = chunk_text(text)
        embeddings = get_embeddings(chunks)
        self.vector_store.add_embeddings(embeddings, chunks)
        print(f"[IngestionAgent] Ingested {file_path}")
