import sys
import os

sys.path.append(os.path.dirname(__file__))
from modules.pdf_uploader import upload_pdf
from modules.pdf_parser import parse_pdf
from modules.qa_module import answer_question
import streamlit as st

def main():
    st.title("AI Web Hosting Program")

    with st.sidebar.title("Navigation"):
        page = st.sidebar.radio("Go to", ["Home", "PDF QA"])
        uploaded_pdf = upload_pdf()
        if uploaded_pdf:
            parsed_content = parse_pdf(uploaded_pdf)
            st.write(parsed_content)
            
            question = st.text_input("Ask a question about the content:")
            if question:
                answer = answer_question(question, parsed_content)
                st.write(answer)

if __name__ == "__main__":
    main()
