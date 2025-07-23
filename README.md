
## 🏁 Getting Started

### 1. Clone the repository

```sh
git clone https://github.com/thejdeep25/Agentic-RAG-Chat-using-MCP.git
cd Agentic-RAG-Chatbot
```

### 2. Set up your environment

It’s recommended to use a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Streamlit app

```sh
cd ui
streamlit run streamlit_app.py
```

### 4. Open your browser

Go to [http://localhost:8501](http://localhost:8501) to use the chatbot.

---

## 📝 Usage

- **Upload a document** (PDF, PPTX, DOCX, CSV, or TXT) in the sidebar.
- **Ask questions** about your document in the chat interface.
- The system will retrieve relevant context and generate answers using the LLM agent.

---

## 🛠️ Customization

- Add new document parsers in `parsers/`.
- Swap out the vector store in `vector_store/`.
- Modify or add agents in `agents/`.

---

## 🤖 Agents

- **IngestionAgent:** Handles document parsing and chunk storage.
- **RetrievalAgent:** Finds relevant chunks for a user query.
- **LLMResponseAgent:** Generates answers using an LLM.

---

## 📦 Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies.

---


## 🙏 Acknowledgements

- Built by Tejdeep Reddy
- Powered by [Streamlit](https://streamlit.io/), [FAISS](https://github.com/facebookresearch/faiss), and [Hugging Face](https://huggingface.co/)

---

*Feel free to contribute or open issues!*
