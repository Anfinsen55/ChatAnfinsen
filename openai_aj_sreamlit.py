from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

import cassio
from PyPDF2 import PdfReader
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import os

# ...

# Define a function to process the user's question and display the result
def process_question(query_text, astra_vector_index, astra_vector_store, llm):
    # print("\nQUESTION: \"%s\"" % query_text)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    # print("ANSWER: \"%s\"\n" % answer)

    # print("FIRST DOCUMENTS BY RELEVANCE:")
    for doc, score in astra_vector_store.similarity_search_with_score(query_text, k=1):
        print(" [%0.4f] \"%s ... \"" % (score, doc.page_content[:84]))

    # Return the results for display
    return answer


# ...

# Streamlit UI
st.title("Chat With Anfinsen")

# Specify the path to the PDF
pdf_path = "C:/Users/Anfinsen/PycharmProjects/Anfinsen/About Me - Anfinsen Joseph.pdf"


# Connect to AstraDB
cassio.init(token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"), database_id=os.getenv("ASTRA_DB_ID"))

# Set up AstraDB and OpenAI components
llm = OpenAI(openai_api_key=os.getenv("OPEN_API_KEY"))
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPEN_API_KEY"))

astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="harry_db",
    session=None,
    keyspace=None,
)

# Load PDF and extract text
pdfreader = PdfReader(pdf_path)
raw_text = ""
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)

texts = text_splitter.split_text(raw_text)
astra_vector_store.add_texts(texts)
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

# Get user's question
user_question = st.text_input("Enter your question:")
if user_question:
    # Process question and display results
    result = process_question(user_question, astra_vector_index, astra_vector_store, llm)

    # Display the result in a more professional format
    st.markdown("## Result")
    # st.success(f"**Question:** {user_question}")
    st.info(f"**Anfinsen: Sir** {result}")

# Run the Streamlit app
if __name__ == "__main__":
    # st.set_page_config(page_title="QA System", page_icon="🔍")
    # st.write("Welcome to the QA System. ")
    pass
