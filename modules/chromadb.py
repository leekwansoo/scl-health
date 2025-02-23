from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="scl_health_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

# Manage Vector store
def load_documents(documents):
    # load documents to the vectorstore
    ids = []
    for document in documents:
        document_id = str(uuid4())
        document = Document(
            document_id=document_id,
            page_content=document.page_content,
            metadata=document.metadata,
        )
        ids.append(document_id)
    #print(documents, ids)
    vector_store.add_documents(documents=documents, ids=ids)
    return "Documents loaded to chromadb successfully"

# add documents to the vectorstore

def add_documents(documents, ids):
    result = vector_store.add_documents(documents = documents, ids =ids)
    # return stored ids of documents
    return result

# delete documents with document ids[]
def delete_documents(ids):
    result = vector_store.delete(ids = ids)
    return result

# search for documents with query
def search_documents(query, k):
    result = vector_store.similarity_search(query = query, k = k)
    return result
    # return document ids[], page_content[], metadata[]