# This parser helps us pull out all the text from Word documents.
from docx import Document

def parse_docx(file_path):
    """
    Opens a DOCX file and grabs the text from every paragraph.
    Returns everything as one big string, separated by newlines.
    """
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])
