# This parser helps us read text from PDF files, one page at a time.
import fitz

def parse_pdf(file_path):
    """
    Opens a PDF and grabs all the text from every page, then puts it together as one big string.
    """
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])
