
import streamlit as st 
import numpy as np 
from modules.vectorstore import search_vectors, store_pdf_content

dim = 128
# Example usage: store and search (this part is just for demonstration, remove in production) 

store_pdf_content("Example content") 
query_embedding = np.random.rand(1, dim).astype('float32') 


results = search_vectors(query_embedding, k=3) 
print(f"Search results: {results}")