# modules/pdf_parser.py

from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
model = "gpt-4o-mini"

def read_pdf(pdf_file):
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
    prompt = f"Please generate questions fromthe given {text}/"
  
    llm = ChatOpenAI(model= model, temperature = 0.2)
    questions = llm.invoke(prompt)
    return questions