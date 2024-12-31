import streamlit as st
from modules.pdf_uploader import upload_pdf
from modules.pdf_parser import parse_pdf
from modules.vectorstore import store_pdf_content, search_vectors

from dotenv import load_dotenv
load_dotenv()
import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from langchain.prompts import PromptTemplate

# DEfine the prompt Template
chat_prompt = PromptTemplate(
    input_variables=['type', 'context'],
    partial_variables={
        'format_instructions': 'The output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{"properties": {"best_article": {"description": "best article you\'ve read", "title": "Best Article", "type": "string"}, "worst_article": {"description": "worst article you\'ve read", "title": "Worst Article", "type": "string"}}, "required": ["best_article", "worst_article"]}\n```'
    },
    template='\n{format_instructions}\n---\nSubjects contained in the PDF documents: {type}\nContext: {context}\n'
)

# Load QA chain
from langchain.chains import LLMChain
from langchain.chains import StuffDocumentsChain
from langchain.llms import OpenAI

# Define the LLM
llm = OpenAI(temperature=0, model="gpt4o-mini")
from langchain.chains import LLMChain

def main():
    # Create the LLM chain 
    llm_chain = LLMChain( llm=llm, prompt=chat_prompt, output_key="response" )

    # Create the QA chain 
    qa_chain = StuffDocumentsChain( llm_chain=llm_chain, document_variable_name="context" )      
        
    st.subheader("Query the PDF Library") 
    query = st.text_input("Enter your question about the uploaded PDFs:") 
    if query: 
        # Run the chain
        # Define the document content and type
        document_content = "This is the content of the document."
        document_type = "PDF"

        # Run the chain
        user_question = "whi is the 36 th president of USA?"
        response = qa_chain.run(messages=[{"role": "user", "content": {user_question}}], context=document_content, type=document_type)
        print(response)


