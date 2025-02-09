# modules/pdf_parser.py

from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
model = "gpt-4o-mini"

def parse_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    page_count = len(reader.pages)
    # extract text from each page
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return page_count, text


from langchain.prompts import PromptTemplate
# 요약문을 작성하기 위한 프롬프트 정의 (직접 프롬프트를 작성하는 경우)

def generate_question(text):
    prompt = f"Please generate questions fromthe given {text}/,the questionnare should be in same language as given text"
  
    llm = ChatOpenAI(model= model, temperature = 0.2)
    questions = llm.invoke(prompt)
    return questions

def create_query_file(file_name, text):
    file_name = file_name.split('.')[0]
    query_file = "query/" + f"{file_name}" + "_query.txt"
    with open(query_file, "w", encoding="utf-8") as f:
        f.write(text)
    return query_file
    
def generate_question_ollama(text):
    llm = ChatOllama(model="llama3.2", temperature = 0.2)
    prompt = ChatPromptTemplate.from_template(
    f"You are a helpful questionnare creator. Please generate 20 questionnares that can be used for query from the context of given{text}/n, the questionnare should be in same language as given text"
    )
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"text": {text}})
    return response