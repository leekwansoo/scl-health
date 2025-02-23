# modules/qa_module.py
import faiss
import numpy as np 
from openai import OpenAI
from modules.chromadb import search_documents, add_documents
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()
import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client=OpenAI()

def answer_question(question, context):
    chat_completion = client.chat.completions.create( messages=[ {"role": "user", "content": question} ], model="gpt-4o-mini", ) 
    return chat_completion.choices[0].message['content'].strip()

import spacy

def create_prompt(query):
    # Load spaCy model
    nlp = spacy.load('en_core_web_md')
    
    # Create embedding for query
    doc = nlp(query)
    query_embedding = doc.vector 
    # Search query
    results = search_documents(query, k=1)
    context = ""
    for result in results:
        context += result.page_content
    # Formulate the prompt
    
    prompt = f"Given the context: {context}\n\nQ: {query}\nA:"
    
    return prompt

def query_library(query):
    prompt = create_prompt(query)
      
    # Generate response using OpenAI 
    chat_completion = client.chat.completions.create( messages=[ {"role": "user", "content": prompt} ], model="gpt-4o-mini", ) 
    
    return chat_completion.choices[0].message






