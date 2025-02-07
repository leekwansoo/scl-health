# Importing necessary modules for vector stores, embeddings, and OpenAI chat models
from langchain_community.vectorstores import FAISS  # Import FAISS for storing and querying vectors
from langchain_openai import OpenAIEmbeddings  # OpenAI embeddings model to generate text embeddings
from langchain_openai import ChatOpenAI  # OpenAI Chat model for conversational AI
from langchain.prompts import ChatPromptTemplate  # Template for generating chat prompts with variables

# Define the template for the prompt that will be used to interact with the OpenAI model
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Function to generate the prompt based on the query text and vector store location
def get_prompt(query_text, vector_store_location):
    # Prepare the database for similarity search by initializing the embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # Use OpenAI model to get embeddings

    # Load the FAISS vector store from a local file, allowing dangerous deserialization for loading purposes
    new_vector_store = FAISS.load_local(
        vector_store_location, embeddings, allow_dangerous_deserialization=True
    )

    # Perform a similarity search with the query text and return results with their similarity scores
    results = new_vector_store.similarity_search_with_score(query_text)

    # If no results were found or the top result has a low similarity score, print a message and return nothing
    if len(results) == 0 or results[0][1] < 0.7:  # Score threshold is set to 0.7 for result relevance
        print(f"Unable to find matching results.")  # Notify if no matching results are found
        return

    # Extract the content of the documents from the similarity search results
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])  # Concatenate document content

    # Create a prompt template based on the pre-defined PROMPT_TEMPLATE
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # Format the prompt by replacing the placeholders {context} and {question} with actual values
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Extract the source metadata from the documents (optional, to track where the content comes from)
    sources = [doc.metadata.get("source", None) for doc, _score in results]  # Collect the source of the documents

    return prompt, sources  # Return the generated prompt and the sources of the documents

# Function to handle a chat history and get a response from OpenAI's chat model
def ask(chat_history):
    print(chat_history)
    # Initialize the OpenAI Chat model (here using a model named 'gpt-4o-mini')
    model = ChatOpenAI(model="gpt-4o-mini")  # Chat model to handle conversation

    # Invoke the model with the given chat history and get the AI-generated message
    ai_msg = model.invoke(chat_history)  # Invoke the model to generate a response

    # Extract the content (the actual response) from the AI message
    response_text = ai_msg.content

    return response_text  # Return the generated response text