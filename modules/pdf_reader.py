# modules/pdf_parser.py

from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import ChatOllama
import os
import json
model = "gpt-4o-mini"
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
embeddings = OpenAIEmbeddings()

def load_pdf(pdf_file):
    loader = PyPDFLoader(pdf_file)
    documents = loader.load()
    split_docs = text_splitter.split_documents(documents)
    # 분할된 텍스트와 임베딩을 사용하여 FAISS 벡터 데이터베이스를 생성합니다.
    return split_docs

def parse_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    page_count = len(reader.pages)
    # extract text from each page
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    split_text = text_splitter.split_text(text)
    return page_count, split_text


from langchain.prompts import PromptTemplate
# 요약문을 작성하기 위한 프롬프트 정의 (직접 프롬프트를 작성하는 경우)

def generate_question(text):
    prompt = f"Please generate questions from the given {text}/,the questionnare should be in same language as given text"
  
    llm = ChatOpenAI(model= model, temperature = 0.2)
    questions = llm.invoke(prompt)
    return questions

def create_query_file(file_name, text):
    file_name = file_name.split('.')[0]
    query_file = "query/" + f"{file_name}" + "_query.txt"
    with open(query_file, "w", encoding="utf-8") as f:
        f.write(text)
    return query_file

def create_qa_file(file_name, qa_pair):
    #print(file_name)
    file_name = file_name.split('_query')[0].split('/')[1]
    #print(file_name)
    qa_file = f"{file_name}" + "_qapair.txt"
    if qa_file not in os.listdir("./qafiles"):
        data_list =[]
        with open(f"qafiles/{qa_file}", "w", encoding="utf-8") as json_file:
            json.dump(data_list, json_file, indent=4, ensure_ascii=False)
    with open(f"qafiles/{qa_file}", "r", encoding="utf-8") as json_file:
        data_list = json.load(json_file)
        data_list.append(qa_pair)
    with open(f"qafiles/{qa_file}", "w", encoding="utf-8") as json_file:
        json.dump(data_list, json_file, indent=4, ensure_ascii=False)
    return qa_file
    
def generate_question_ollama(text):
    llm = ChatOllama(model="llama3.2", temperature = 0.2)
    prompt = ChatPromptTemplate.from_template(
    f"You are a helpful questionnare creator. Please generate 20 questionnares that can be used for query from the context of given{text}/n, the questionnare should be in same language as given text"
    )
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"text": {text}})
    return response