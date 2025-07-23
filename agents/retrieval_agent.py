# This agent is like your research assistant—it finds the most relevant parts of your documents for any question you ask!
from embeddings.embedder import get_embeddings
from mcp.message_dispatcher import MCPMessage

class RetrievalAgent:
    def __init__(self, dispatcher, vector_store):
        """
        Set up the RetrievalAgent with access to the dispatcher and the vector store.
        Registers itself so it can respond to search requests from the UI or other agents.
        """
        self.dispatcher = dispatcher
        self.vector_store = vector_store
        dispatcher.register_agent("RetrievalAgent", self.handle)

    def handle(self, message):
        """
        When a question comes in, this method:
        1. Turns the question into an embedding (a math-y representation)
        2. Searches the vector store for the most relevant document chunks
        3. Packages up the results and sends them to the LLMResponseAgent
        """
        query = message.payload["query"]
        query_embedding = get_embeddings([query])[0]
        top_chunks = self.vector_store.search(query_embedding)
        response = MCPMessage(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            type="RETRIEVAL_RESULT",
            trace_id=message.trace_id,
            payload={"retrieved_context": top_chunks, "query": query}
        )
        self.dispatcher.send_message(response)
