# modules/vectorstore.py
import numpy as np
import pickle
from config import VECTORSTORE_PATH, METADATA_PATH
import faiss

# Initialize FAISS index (change dim to match your embedding size)
dim = 128
#index = faiss.IndexFlatL2(dim)

# Load existing index and metadata if available
try:
    index = faiss.read_index(VECTORSTORE_PATH)
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.load(f)
except FileNotFoundError:
    print("Index or metadata file not found. Initializing new index and metadata.")
    index = faiss.IndexFlatL2(dim)
    metadata = []
    
except Exception as e: 
    print(f"An error occurred while loading index or metadata: {e}")     
    index = faiss.IndexFlatL2(dim) 
    metadata = []

def store_pdf_content(content):
    # Create embedding (replace with actual embedding model)
    embedding = np.random.rand(1, dim).astype('float32')
    
    # Add to index and metadata
    index.add(embedding)
    metadata.append(content)
    
    # Save updated index and metadata
    faiss.write_index(index, VECTORSTORE_PATH)
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
    message = "Contents stored in vectoestore"
    return message


def search_vectors(query_embedding, k=3):
    distances, indices = index.search(query_embedding, k)
    print(indices)
    results = [metadata[i] for i in indices[0]]
    return results
