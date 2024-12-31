# modules/pdf_uploader.py
import streamlit as st
import PyPDF2
from modules.vectorstore import store_pdf_content

def upload_pdf():
    uploaded_file_1= st.file_uploader("Upload a PDF", type="pdf", key = "file_1")
    if uploaded_file_1 is not None:
        return uploaded_file_1
    return None

def parse_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content

