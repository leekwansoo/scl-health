# modules/pdf_parser.py
import PyPDF2

def parse_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content