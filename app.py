import streamlit as st 
import io
import os
import json 
from modules.pdf_reader import generate_question
from modules.pdf_parser import parse_pdf
from modules.vectorstore import store_pdf_content
from modules.query_handler import query_library
from doc_handler import add_document, retrieve_document, list_documents, check_document
from graph import get_weather, search_web
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
st.title("Webzine for SCL Health")
path = "data/file_uploaded"

# Create a sidebar for navigation
st.sidebar.title("Menu")
options = st.sidebar.radio("Select an option", ["Upload File", "Web Search"])

if options == "Upload File":
    st.sidebar.header("Upload File")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf", key="pdf_uploader")
       
    if uploaded_file:
        file_name = uploaded_file.name
        page_count, parsed_file = parse_pdf(uploaded_file)
        questions= generate_question(parsed_file)
        st.sidebar.markdown(questions.content)
        check_exist = check_document(file_name)
        if check_exist == "noexist":
            result = store_pdf_content(parsed_file)
            if result:
                st.sidebar.write(result)
                add_document(file_name)     
            else: st.sidebar.write("storing PDF file into vector store failed")
        
            docs = list_documents()
            if docs:
                for doc in docs:
                    st.sidebar.write(f"Uploaded_Document: {doc}\n")  
            else:
                st.sidebar.write("There are no Uploaded Documents")     
        
        else:
            st.write(f"{file_name} is already stored in the vectorstore") 
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
    #st.markdown(json_data)


