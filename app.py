import streamlit as st 
import io
import os
import json 
from modules.pdf_reader import generate_question, parse_pdf, generate_question_ollama, create_query_file
from modules.vectorstore import store_pdf_content
from modules.query_handler import query_library
from doc_handler import add_document, retrieve_document, list_documents, check_document
from graph import search_web
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
st.title("Webzine for SCL Health")

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
        # store the file in the uploaded file folder
        uploaded_name = f"uploaded/{file_name}"
        with open(uploaded_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        page_count, parsed_file = parse_pdf(uploaded_file)
        questions= generate_question(parsed_file)
        query_file = create_query_file(file_name, questions.content)
        st.session_state["query_file"].append(query_file)
        for question in questions.content:
            st.session_state["query_message"].append(question)
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
            
elif options == "Query from Uploaded File":
    st.header("Query from Uploaded File")
    query_list = os.listdir("query")
    selected = st.sidebar.selectbox("Select month to query", query_list)
    file_name = f"query/{selected}"
    with open(file_name, "r", encoding="utf-8") as f:
        s = f.read()
        st.sidebar.markdown(s)
     
    
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


