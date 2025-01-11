# modules/pdf_uploader.py

import streamlit as st

def upload_pdf():
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        return uploaded_file
    return None
