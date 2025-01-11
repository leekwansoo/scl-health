import PyPDF2
from PyPDF2 import PdfReader
def read_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    # extract text from each page
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text