import streamlit as st
from PyPDF2 import PdfReader 
import io
from modules.pdf_uploader import upload_pdf
from modules.text_embedder import embed_text
from modules.vectorstore import store_pdf_content, search_vectors
from modules.query_handler import query_library
from doc_handler import add_document, retrieve_document, list_documents
st.title("Webzine for SCL Health")

 
# Sidebar setup
st.sidebar.header("Menu")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf", key="pdf_uploader")
prompts = ["Mathematics", "Science", "History", "Literature"]
prompt_selected = st.sidebar.selectbox("Select Prompt", ["Mathematics", "Science", "History", "Literature"], key="subject_select")
st.write(f"Selected Prompt: {prompt_selected}")


# Function to read PDF and extract text
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    num_page = pdf_reader.pages

    for page in num_page:
        text += page.extract_text()
    return text

# Main content

if uploaded_file:
    file_name = uploaded_file.name
    pdf_text = read_pdf(uploaded_file)
    parsed_file = parse_pdf(uploaded_file)
    result = store_pdf_content(parsed_file)
    if result:
        st.sidebar.write(result)
        add_document("doc1", {file_name} )
    else: st.sidebar.write("storing PDF file into vector store failed")
    
else:
    st.sidebar.write("Please upload a PDF and select subject to get started.")

    
st.header("Query the PDF Library") 
query = st.text_input("Enter your question for your selected subject:") 
if query: 
    # Run the chain
    # Define the document content and type
    document_content = "This is the content of the document."
    document_type = "PDF"
    
    response = query_library(query)
    print(response)
    
    st.write(response)

