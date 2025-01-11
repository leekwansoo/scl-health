import streamlit as st

st.title("Webzine for SCL Health")

if "DOCUMENT" not in st.session_state: 
    st.session_state["DOCUMENT"] = {"key": ""}

#if st.session_state["DOCUMENT"] is None:
#   st.session_state["DOCUMENT"] = {"key": ""}
    
# Function to add data to DOCUMENT directory 
def add_document(key, value): 
    st.session_state["DOCUMENT"][key] = value 
    st.write(f"Document added: {key} -> {value}") 
# Function to retrieve data from DOCUMENT directory 
def retrieve_document(key): 
    if key in st.session_state["DOCUMENT"]: 
        return st.session_state["DOCUMENT"][key] 
    else: st.write(f"Document with key '{key}' not found.") 
    return None 
# Example usage # List Document
def list_documents(): 
    if st.session_state["DOCUMENT"]:
        docs = []
        st.write("Documents in 'DOCUMENT':") 
        for key, value in st.session_state["DOCUMENT"].items(): 
            doc = {key : value}
            docs.append(doc)
            st.write(f"{key}: {value}") 
        return(docs)
    else: st.write("No documents found in 'DOCUMENT'.")

"""
# Adding data 
add_document("doc1", "This is the content of document 1.")\n 
add_document("doc2", "This is the content of document 2.") 

# Retrieving data 
retrieve_document("doc1")\n 
"""