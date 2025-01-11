from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_community.callbacks.manager import get_openai_callback
from pydantic import Field, BaseModel

from dotenv import load_dotenv
load_dotenv()
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

llm = ChatOpenAI(
    openai_api_key='',
    model_name="gpt-4o",
    response_format={"type": "json_object"},
)

template = """
{format_instructions}
---
Subjects contained in the PDF documents: {type}
"""
class Response(BaseModel):
    best_article: str = Field(description="best article you've read")
    worst_article: str = Field(description="worst article you've read")
    
parser = PydanticOutputParser(pydantic_object=Response)

st.title('💬PDF Summarizer and Q/A App')

pdf = st.sidebar.file_uploader("Upload your PDF File and Ask Questions", type="pdf")
if pdf is not None:
    
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        
    # split into chunks
    text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    #create embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    
    # show user input
    with st.chat_message("user"):
        st.write("Hello World👋")
        user_question = st.text_input("Please ask a question about your PDF here:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question, k=2)
            print(docs)           
            system_message = SystemMessage(content="You are a librian to analyze PDF documents and explain the contents of the documents.")
            human_message = HumanMessagePromptTemplate.from_template(template=template,
                                                         input_variables=docs,
                                                         partial_variables={
                                                             "format_instructions": parser.get_format_instructions()})
            st.write(human_message)
            chat_prompt = ChatPromptTemplate.from_messages([system_message, MessagesPlaceholder(variable_name="messages")])
            st.write(chat_prompt)
            
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)
                
            st.write(response)