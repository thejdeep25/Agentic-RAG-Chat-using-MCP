import cohere
import streamlit as st  # ✅ added this

# This agent is the "answer writer"—it takes the context and your question, and crafts a response using the LLM.
# Think of it as the helpful expert who reads your notes and gives you a clear answer!

# Initialize Cohere client with your API key
co = cohere.Client("UPCowgiMPtKn1fI04uJGEjWVGm9dY9kLqXS9m3PD")

class LLMResponseAgent:
    def __init__(self, dispatcher):
        """
        Set up the LLMResponseAgent and register it so it can handle answer requests.
        """
        self.dispatcher = dispatcher
        dispatcher.register_agent("LLMResponseAgent", self.handle)

    def handle(self, message):
        """
        When a context and question arrive, this method:
        1. Builds a prompt for the LLM using the context and question
        2. Calls the Cohere LLM to generate an answer
        3. Saves the answer to Streamlit session state for the UI to display
        """
        context = message.payload["retrieved_context"]
        query = message.payload["query"]

        # Formulate prompt combining context and user query
        prompt = f"Context:\n{context}\n\nQuestion: {query}"

        # Call Cohere LLM
        response = co.generate(
            model="command-r-plus",  # Or 'command' if on free tier
            prompt=prompt,
            max_tokens=300,
            temperature=0.3
        )

        # Safety check for generations response
        if response.generations:
            answer = response.generations[0].text.strip()

            # ✅ Save result to Streamlit session state
            st.session_state["llm_response"] = answer

            print("Answer:", answer)  # optional for terminal log
        else:
            st.session_state["llm_response"] = "No response generated."
            print("No response generated.")
