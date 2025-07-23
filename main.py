# This is the main entry point for the backend system.
# It sets up all the agents, the dispatcher, and the vector store—think of it as the "stage manager" for the whole show!
from mcp.message_dispatcher import MCPDispatcher
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from vector_store.faiss_store import VectorStore
import parsers.pdf_parser as pdf
import parsers.pptx_parser as pptx
import parsers.docx_parser as docx
import parsers.csv_parser as csv
import parsers.txt_parser as txt
from mcp.message_dispatcher import MCPMessage

# Set up the core system components
dispatcher = MCPDispatcher()
vector_store = VectorStore(dim=384)

# All the file parsers in one place
parsers = {
    "pdf": pdf.parse_pdf,
    "pptx": pptx.parse_pptx,
    "docx": docx.parse_docx,
    "csv": csv.parse_csv,
    "txt": txt.parse_txt
}

# Register the agents so they can work together
IngestionAgent(dispatcher, vector_store, parsers)
RetrievalAgent(dispatcher, vector_store)
LLMResponseAgent(dispatcher)

