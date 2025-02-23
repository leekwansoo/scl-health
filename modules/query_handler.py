# modules/qa_module.py

from openai import OpenAI
from modules.chromadb import search_similarity
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()
import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client=OpenAI()

def answer_question(question, context):
    chat_completion = client.chat.completions.create( messages=[ {"role": "user", "content": question} ], model="gpt-4o-mini", ) 
    return chat_completion.choices[0].message['content'].strip()


def create_prompt(query):   
    # Search query
    results = search_similarity(query, k=1)
    context = ""
    for result in results:
        context += result.page_content
    # Formulate the prompt
    
    prompt = f"Given the context: {context}\n\nQ: {query}\nA:"
    
    return prompt

def query_library(query):
    prompt = create_prompt(query)
    print(prompt) 
    # Generate response using OpenAI 
    chat_completion = client.chat.completions.create( messages=[ {"role": "user", "content": prompt} ], model="gpt-4o-mini", ) 
    
    return chat_completion.choices[0].message

