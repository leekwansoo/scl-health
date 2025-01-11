# SELF QUERY HANDLER

from langchain.chains.query_constructor import SelfQueryRetriever
from langchain.prompts import SelfQueryPrompt
from langchain.prompts import PromptTemplate
from modules.text_embedder import split_text
# Define a prompt template for the self query
context = """What are the main topics dicussed in this month's issue of the magazine 건강생활?"""
prompt_template = PromptTemplate(
    input_variables=["query", "context", "metadata"],
    template="Use the following context to generate a query: {context}\nQuery: {query}",
    metadata={"context": "The meaning of life is"}
)

text = prompt_template
retriever=SelfQueryRetriever(
    vectorstore=split_text(text).vectorstore,
    llm_chain=prompt_template,
    verbose=True
)
result = retriever.get_relevant_documents("What are the main topics dicussed in this month's issue of the magazine 건강생활?")

for doc in result:
    print(doc.text)
    print(doc.page_content)
    print(doc.metadata)
    print("\n\n")