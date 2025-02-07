# modules/pdf_parser.py

from PyPDF2 import PdfReader
def parse_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    page_count = len(reader.pages)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return page_count, content