import streamlit as st 
import io
import json 
from modules.pdf_parser import parse_pdf
from modules.vectorstore import store_pdf_content, search_vectors
from modules.query_handler import query_library
from doc_handler import add_document, retrieve_document, list_documents
from graph import get_weather, search_web

st.title("Webzine for SCL Health")


# Create a sidebar for navigation
st.sidebar.title("Menu")
options = st.sidebar.radio("Select an option", ["Upload File", "Web Search"])

if options == "Upload File":
    st.sidebar.header("Upload File")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf", key="pdf_uploader")
    prompts = ["Mathematics", "Science", "History", "Literature"]
    prompt_selected = st.sidebar.selectbox("Select Prompt", ["Mathematics", "Science", "History", "Literature"], key="subject_select")
    st.write(f"Selected Prompt: {prompt_selected}")
    
    if uploaded_file:
        file_name = uploaded_file.name
        parsed_file = parse_pdf(uploaded_file)
        result = store_pdf_content(parsed_file)
        if result:
            st.sidebar.write(result)
            add_document("doc1", {file_name} )
        else: st.sidebar.write("storing PDF file into vector store failed")
        
    else:
        st.sidebar.write("Please upload a PDF and select subject to get started.")
    
elif options == "Web Search":
    st.header("Web Search")
    query = st.text_input("Enter a search query:")
    if st.button("Search Web"):
        if query:
            results = search_web(query)
            for result in results:
                st.write(result["content"])
        else:
            st.write("Please enter a search query.")
    
# Main Page content
   
st.header("Query the PDF Library") 
query = st.text_input("Enter your question for your uploaded documents:") 
if query: 
    # Define the document content and type
    document_content = "This is the content of the document."
    document_type = "PDF"    
    response = query_library(query)
    print(response)
    
   
    st.write(response.content)
    
    # import json
   
    data = response
    list_data = list(data)
    json_data = json.dumps(list_data, ensure_ascii=False)
    print("this is json data")
    print(json_data)
    # Create a Markdown string
       # Print the Markdown string
    st.markdown(json_data)


