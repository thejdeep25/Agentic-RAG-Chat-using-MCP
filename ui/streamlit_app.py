import sys
import os
import time

# --- Project Path Setup ---
# (We want to make sure we can import everything, no matter where we run this from)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
print("Python PATH:", sys.path)
print("Working dir:", os.getcwd())

# --- Core Imports ---
from mcp.message_dispatcher import MCPDispatcher, MCPMessage
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from vector_store.faiss_store import VectorStore
import parsers.pdf_parser as pdf
import parsers.pptx_parser as pptx
import parsers.docx_parser as docx
import parsers.csv_parser as csv
import parsers.txt_parser as txt
import streamlit as st

# === System Initialization ===
# Set up the dispatcher (message hub) and the vector store (memory for document chunks)
dispatcher = MCPDispatcher()
vector_store = VectorStore(dim=384)
parsers_dict = {
    "pdf": pdf.parse_pdf,
    "pptx": pptx.parse_pptx,
    "docx": docx.parse_docx,
    "csv": csv.parse_csv,
    "txt": txt.parse_txt
}

# Register all the agents so they can talk to each other
IngestionAgent(dispatcher, vector_store, parsers_dict)
RetrievalAgent(dispatcher, vector_store)
LLMResponseAgent(dispatcher)

# === UI Styling (unchanged) ===
st.markdown("""
<style>
/* Import clean, modern font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Remove default Streamlit styling */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* Global Variables */
:root {
    --primary-color: #2563eb;
    --background: #ffffff;
    --surface: #ffffff;
    --text-primary: #2563eb;
    --text-secondary: #2563eb;
    --border: #e2e8f0;
    --success: #10b981;
    --info: #3b82f6;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --radius: 8px;
    --radius-lg: 12px;
}

/* App Container */
.stApp {
    background-color: var(--background);
    font-family: 'Inter', sans-serif;
}

.main > div {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

/* Header */
.app-header {
    text-align: center;
    margin-bottom: 3rem;
    padding: 2rem 0;
}

.app-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    line-height: 1.2;
    background: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    letter-spacing: 1px;
}

.app-subtitle {
    font-size: 1.1rem;
    color: var(--text-primary);
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Cards */
.card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: none;
    border: 1px solid var(--border);
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.card-icon {
    width: 20px;
    height: 20px;
    margin-right: 0.75rem;
    color: var(--primary-color);
}

.card-description {
    color: var(--text-primary);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    line-height: 1.5;
}

/* File Upload Styling */
.stFileUploader {
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 2rem !important;
    background: var(--background) !important;
    transition: all 0.2s ease !important;
}

.stFileUploader:hover {
    border-color: var(--primary-color) !important;
    background: #f5faff !important;
}

.stFileUploader > div {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    text-align: center !important;
}

.stFileUploader label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* Text Input */
.stTextInput > div > div > input {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary-color) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px #e3edff !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--text-primary) !important;
}

/* Text Area */
.stTextArea > div > div > textarea {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    line-height: 1.6 !important;
    resize: vertical !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-color) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px #e3edff !important;
}

.stTextArea > div > div > textarea::placeholder {
    color: var(--text-primary) !important;
}

/* Success and Info Messages */
.stSuccess, .stInfo {
    background: #f5faff !important;
    border: 1px solid #e3edff !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Spinner */
.stSpinner {
    text-align: center !important;
}

.stSpinner > div {
    border-color: var(--primary-color) !important;
}

/* Expander */
.stExpander {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
}

.stExpander > div > div {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}

/* Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

.status-success {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success);
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-processing {
    background: rgba(59, 130, 246, 0.1);
    color: var(--info);
    border: 1px solid rgba(59, 130, 246, 0.2);
}

/* Responsive Design */
@media (max-width: 768px) {
    .main > div {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .app-title {
        font-size: 2rem;
    }
    
    .card {
        padding: 1.5rem;
    }
}

/* Clean scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--background);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
}
</style>
""", unsafe_allow_html=True)

# Add a global CSS override to force all text to black
st.markdown("""
<style>
body, .stApp, .main, .block-container, .sidebar .sidebar-content, .stSidebar, .stSidebar *, .stTextInput, .stTextArea, .stFileUploader, .stSuccess, .stInfo, .stExpander, .stExpander *, .stMarkdown, .stAlert, .stButton, .stSelectbox, .stRadio, .stCheckbox, .stSlider, .stNumberInput, .stDateInput, .stTimeInput, .stColorPicker, .stMultiSelect, .stText, .stDataFrame, .stTable, .stJson, .stCode, .stCaption, .stMetric, .stHeader, .stSubheader, .stTitle, .stFooter, .stSidebar, .stSidebar *, .stMarkdown *, .stAlert *, .stButton *, .stSelectbox *, .stRadio *, .stCheckbox *, .stSlider *, .stNumberInput *, .stDateInput *, .stTimeInput *, .stColorPicker *, .stMultiSelect *, .stText *, .stDataFrame *, .stTable *, .stJson *, .stCode *, .stCaption *, .stMetric *, .stHeader *, .stSubheader *, .stTitle *, .stFooter *, .stSidebar * {
    color: #111 !important;
}

.chat-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem 0 6rem 0;
    min-height: 70vh;
}
.user-bubble {
    background: #2563eb;
    color: #111 !important;
    border-radius: 18px 18px 4px 18px;
    padding: 1rem 1.2rem;
    margin: 1rem 0 0.5rem auto;
    max-width: 80%;
    font-size: 1.08rem;
    box-shadow: 0 2px 8px #2563eb22;
    text-align: right;
}
.agent-bubble {
    background: #fff;
    color: #111 !important;
    border-radius: 18px 18px 18px 4px;
    padding: 1rem 1.2rem;
    margin: 0.5rem auto 1rem 0;
    max-width: 80%;
    font-size: 1.08rem;
    box-shadow: 0 2px 8px #e2e8f022;
    border: 1px solid #e2e8f0;
    text-align: left;
}
.chat-input-container {
    position: fixed;
    left: 0; right: 0; bottom: 0;
    background: #f7f7fa;
    border-top: 1.5px solid #e2e8f0;
    padding: 1.2rem 0.5rem 1.2rem 0.5rem;
    z-index: 100;
    width: 100vw;
    box-shadow: 0 -2px 12px #2563eb11;
}
.chat-input-box {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    display: flex;
    gap: 0.5rem;
}
.stTextInput > div > div > input {
    font-size: 1.1rem !important;
    padding: 0.8rem 1.2rem !important;
    border-radius: 18px !important;
    border: 1.5px solid #2563eb !important;
    color: #111 !important;
    background: #fff !important;
}
.stTextInput > div > div > input::placeholder {
    color: #111 !important;
}
.stButton > button {
    background: #2563eb !important;
    color: #fff !important;
    border-radius: 18px !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 1.5rem !important;
    border: none !important;
    box-shadow: 0 2px 8px #2563eb22;
}
.stButton > button:hover {
    background: #003399 !important;
}
.stSidebar, .stSidebar * {
    background: #f7f7fa !important;
    color: #111 !important;
}
.stSuccess, .stInfo {
    background: #fff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #111 !important;
    font-family: 'Inter', sans-serif !important;
}
.stExpander > div > div {
    color: #111 !important;
}
.stFileUploader > div, .stFileUploader label {
    color: #111 !important;
}
.stTextArea > div > div > textarea, .stTextArea > div > div > textarea::placeholder {
    color: #111 !important;
}
.stMarkdown, .stMarkdown * {
    color: #111 !important;
}
.stAlert, .stAlert * {
    color: #111 !important;
}
.stButton, .stButton * {
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# Update global CSS for sidebar and borders
st.markdown("""
<style>
body, .stApp, .main, .block-container {
    background: #f7f7fa !important;
    color: #111 !important;
}

.stSidebar, .sidebar .sidebar-content {
    background: #fff !important;
    color: #111 !important;
    border-right: 1.5px solid #111 !important;
}

.sidebar-box, .sidebar-system-box {
    background: #fff;
    border: 1.5px solid #111;
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 1.2rem;
}

.stFileUploader {
    background: #fff !important;
    border: 1.5px solid #111 !important;
    border-radius: 12px !important;
}

.chat-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem 0 6rem 0;
    min-height: 70vh;
}
.user-bubble {
    background: #f3f4f6 !important;
    color: #111 !important;
    border-radius: 18px 18px 4px 18px;
    padding: 1rem 1.2rem;
    margin: 1rem 0 0.5rem auto;
    max-width: 80%;
    font-size: 1.08rem;
    box-shadow: none;
    border: 1.5px solid #111;
    text-align: right;
}
.agent-bubble {
    background: #fff;
    color: #111 !important;
    border-radius: 18px 18px 18px 4px;
    padding: 1rem 1.2rem;
    margin: 0.5rem auto 1rem 0;
    max-width: 80%;
    font-size: 1.08rem;
    box-shadow: none;
    border: 1.5px solid #111;
    text-align: left;
}
.chat-input-container {
    position: fixed;
    left: 0; right: 0; bottom: 0;
    background: #f7f7fa;
    border-top: 1.5px solid #e2e8f0;
    padding: 1.2rem 0.5rem 1.2rem 0.5rem;
    z-index: 100;
    width: 100vw;
    box-shadow: 0 -2px 12px #2563eb11;
}
.chat-input-box {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    display: flex;
    gap: 0.5rem;
    border: 1.5px solid #111;
    border-radius: 18px;
    background: #111;
    padding: 0.3rem 0.5rem;
}
.stTextInput > div > div > input {
    font-size: 1.1rem !important;
    padding: 0.8rem 1.2rem !important;
    border-radius: 18px !important;
    border: none !important;
    color: #fff !important;
    background: #111 !important;
}
.stTextInput > div > div > input::placeholder {
    color: #fff !important;
}
.stButton > button {
    background: #111 !important;
    color: #fff !important;
    border-radius: 18px !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 1.5rem !important;
    border: none !important;
    box-shadow: none;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #333 !important;
}
.stSuccess, .stInfo {
    background: #fff !important;
    border: 1.5px solid #111 !important;
    border-radius: 8px !important;
    color: #111 !important;
    font-family: 'Inter', sans-serif !important;
}
.stExpander > div > div {
    color: #111 !important;
}
.stFileUploader > div, .stFileUploader label {
    color: #111 !important;
}
.stTextArea > div > div > textarea, .stTextArea > div > div > textarea::placeholder {
    color: #111 !important;
}
.stMarkdown, .stMarkdown * {
    color: #111 !important;
}
.stAlert, .stAlert * {
    color: #111 !important;
}
.stButton, .stButton * {
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# --- Chatbot UI Redesign ---

# Sidebar: where users upload files and see system status
with st.sidebar:
    st.markdown("""
    <div class='sidebar-box'>
        <h2 style='color:#111;'>⧉ Tej's Agentic RAG Pro System</h2>
        <div style='color:#111; font-size:1.05rem;'>The next-gen, interactive, pro-level RAG chatbot for your documents.<br><span style='font-size:1rem;'>Made by Tej 🚀</span></div>
    </div>
    <div class='sidebar-box'>
        <div style='margin-top:0; color:#111; font-weight:600;'>Document Upload</div>
        <div style='color:#111; font-size:0.95rem;'>Supports PDF, PPTX, DOCX, CSV, TXT</div>
    </div>
    """, unsafe_allow_html=True)
    # User uploads a file here; we process it and let the agents know
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "pptx", "docx", "csv", "txt"])
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]
        temp_path = f"temp_upload.{file_type}"
        with st.spinner("Processing your document, hang tight!"):
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Send a message to the IngestionAgent to start processing
            ingestion_msg = MCPMessage(
                sender="UI",
                receiver="IngestionAgent",
                type="DOCUMENT_UPLOAD",
                trace_id="trace-001",
                payload={"file_path": temp_path, "file_type": file_type}
            )
            dispatcher.send_message(ingestion_msg)
        # Show a custom message to the user (invisible text on white, as requested)
        st.markdown(f"""
        <div style='background:#fff; color:#fff; border:1.5px solid #111; border-radius:8px; padding:1rem 1.2rem; font-family:Inter,sans-serif; margin-bottom:1.2rem;'>
        ✅ Document '{uploaded_file.name}' successfully processed and indexed
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <div class='sidebar-system-box'>
        <b>System Status</b><br>
        Vector Store: Active (384 dims)<br>
        Supported: PDF, PPTX, DOCX, CSV, TXT<br>
        Agents: Ingestion, Retrieval, LLM Response<br>
        Dispatcher: Running
    </div>
    """, unsafe_allow_html=True)

# Main chat area: where the conversation happens
st.markdown("""
<style>
.chat-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem 0 6rem 0;
    min-height: 70vh;
}
.user-bubble {
    background: #2563eb;
    color: #111 !important;
    border-radius: 18px 18px 4px 18px;
    padding: 1rem 1.2rem;
    margin: 1rem 0 0.5rem auto;
    max-width: 80%;
    font-size: 1.08rem;
    box-shadow: 0 2px 8px #2563eb22;
    text-align: right;
}
.agent-bubble {
    background: #fff;
    color: #111 !important;
    border-radius: 18px 18px 18px 4px;
    padding: 1rem 1.2rem;
    margin: 0.5rem auto 1rem 0;
    max-width: 80%;
    font-size: 1.08rem;
    box-shadow: 0 2px 8px #e2e8f022;
    border: 1px solid #e2e8f0;
    text-align: left;
}
.chat-input-container {
    position: fixed;
    left: 0; right: 0; bottom: 0;
    background: #f7f7fa;
    border-top: 1.5px solid #e2e8f0;
    padding: 1.2rem 0.5rem 1.2rem 0.5rem;
    z-index: 100;
    width: 100vw;
    box-shadow: 0 -2px 12px #2563eb11;
}
.chat-input-box {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    display: flex;
    gap: 0.5rem;
}
.stTextInput > div > div > input {
    font-size: 1.1rem !important;
    padding: 0.8rem 1.2rem !important;
    border-radius: 18px !important;
    border: 1.5px solid #2563eb !important;
    color: #111 !important;
    background: #fff !important;
}
.stButton > button {
    background: #2563eb !important;
    color: #fff !important;
    border-radius: 18px !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 1.5rem !important;
    border: none !important;
    box-shadow: 0 2px 8px #2563eb22;
}
.stButton > button:hover {
    background: #003399 !important;
}
</style>
<div class='chat-container'>
""", unsafe_allow_html=True)

# Chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Show chat bubbles for each message in the conversation
for entry in st.session_state["chat_history"]:
    if entry["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{entry['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='agent-bubble'>{entry['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Chat input at the bottom: user types a question and hits send
with st.container():
    st.markdown("""
    <div class='chat-input-container'>
      <form action="#" method="post">
        <div class='chat-input-box'>
    """, unsafe_allow_html=True)
    user_input = st.text_input("Your question", "", key="chat_input", label_visibility="collapsed", placeholder="type your msg n press enter", help=None)
    send = st.button("Send", key="send_btn")
    st.markdown("""
        </div>
      </form>
    </div>
    """, unsafe_allow_html=True)

# --- Chat Logic ---
# When the user sends a message, add it to the chat history and trigger the agents
if send and user_input.strip():
    st.session_state["chat_history"].append({"role": "user", "content": user_input.strip()})
    if not uploaded_file:
        st.session_state["chat_history"].append({"role": "agent", "content": "Please upload a document before asking a question."})
    else:
        # Build a message for the RetrievalAgent to fetch relevant context
        retrieval_msg = MCPMessage(
            sender="UI",
            receiver="RetrievalAgent",
            type="QUERY_REQUEST",
            trace_id="trace-002",
            payload={"query": user_input.strip()}
        )
        dispatcher.send_message(retrieval_msg)
        # Wait for the LLMResponseAgent to put the answer in session state
        import time
        for _ in range(30):
            if "llm_response" in st.session_state:
                break
            time.sleep(0.1)
        if "llm_response" in st.session_state:
            st.session_state["chat_history"].append({"role": "agent", "content": st.session_state["llm_response"]})
            del st.session_state["llm_response"]
        else:
            st.session_state["chat_history"].append({"role": "agent", "content": "Sorry, no response generated."})
    st.experimental_rerun()
