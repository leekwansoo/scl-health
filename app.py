import streamlit as st 
import io
import os
import json 
from modules.pdf_reader import generate_question, parse_pdf, create_query_file, load_pdf, create_qa_file
from modules.vectorstore import store_pdf_content
from modules.chromadb import load_documents
from modules.query_handler import query_library
from doc_handler import add_document, retrieve_document, list_documents, check_document
from graph import search_web
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
st.title("Webzine for SCL Health")

# Main Page content 
def main_query():
    query = st.text_input("Enter your question for your uploaded documents:") 
    if query: 
        response = query_library(query)
        if response:
            qa_pair = {"query": query, "answer": response.content}
            qa_file = create_qa_file(file_name, qa_pair)
            st.write(response.content)
            st.write(f"QA pair is saved in {qa_file}")
        
st.session_state["query_message"] = []
st.session_state["query_file"] = []

# Create a sidebar for navigation
st.sidebar.title("Menu")
options = st.sidebar.radio("Select an option", ["Upload File", "Query from Uploaded File", "Web Search"])

if options == "Upload File":
    st.sidebar.header("Upload File")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf", key="pdf_uploader")
       
    if uploaded_file:
        file_name = uploaded_file.name
        # check_exist = check_document(file_name)
        check_exist = "noexist"
        if check_exist == "noexist":
            # store the file in the uploaded file folder
            uploaded_name = f"uploaded/{file_name}"
            with open(uploaded_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            page_count, split_text = parse_pdf(uploaded_file)
            #result = store_pdf_content(split_text)
            documents = load_pdf(uploaded_name)
            result = load_documents(documents)
            if result:
                st.sidebar.write(result)
                add_document(file_name)     
            else: st.sidebar.write("storing PDF file into vector store failed")
            questions= generate_question(split_text)
            query_file = create_query_file(file_name, questions.content)
            st.session_state["query_file"].append(query_file)
            for question in questions.content:
                st.session_state["query_message"].append(question)
            st.sidebar.markdown(questions.content)
                      
            docs = list_documents()
            if docs:
                for doc in docs:
                    st.sidebar.write(f"Uploaded_Document: {doc}\n")  
        else:
            st.sidebar.write(f"{file_name} is aleardy uploaded\n")     
         
    else:
        st.sidebar.write("Please upload a PDF and select subject to get started.")
        
    main_query()
            
elif options == "Query from Uploaded File":
    st.header("Query from Uploaded File")
    query_list = os.listdir("query")
    selected = st.sidebar.selectbox("Select month to query", query_list)
    file_name = f"query/{selected}"
    with open(file_name, "r", encoding="utf-8") as f:
        s = f.read()
        st.sidebar.markdown(s)
        
    main_query() 
          
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