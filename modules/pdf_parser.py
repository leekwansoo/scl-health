# modules/pdf_parser.py

import PyPDF2

def parse_pdf(uploaded_pdf):
    reader = PyPDF2.PdfReader(uploaded_pdf)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content
