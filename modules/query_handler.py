# modules/qa_module.py
import openai
from openai import OpenAI
from modules.vectorstore import search_vectors
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client=OpenAI()

def answer_question(question, context):
    chat_completion = client.chat.completions.create( messages=[ {"role": "user", "content": question} ], model="gpt-4o-mini", ) 
    return chat_completion.choices[0].message['content'].strip()

def query_library(query):
    # Create embedding for query (replace with actual embedding model) 
    query_embedding = np.random.rand(1, 128).astype('float32') 
    # Search vectors 
    results = search_vectors(query_embedding) 
    # Formulate the prompt 
    context = ' '.join(results) 
    prompt = f"Given the context: {context}\n\nQ: {query}\nA:" 
    print(context)
    # Generate response using OpenAI 
    chat_completion = client.chat.completions.create( messages=[ {"role": "user", "content": prompt} ], model="gpt-4o-mini", ) 
    
    return chat_completion.choices[0].message
