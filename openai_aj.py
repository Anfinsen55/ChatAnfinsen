from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from datasets import load_dataset

import cassio

from PyPDF2 import PdfReader

ASTRA_DB_APPLICATION_TOKEN = "AstraCS:memuPzmNDRjXUNXmfxzgpLBQ:045218cb573cfb50b2a58bb91e3b0185f779888c03a412dae5ac97ca92a6bf5a"  # click on generate token and copy the token
ASTRA_DB_ID = "ef4e67d3-2ec3-496d-baf9-6be34fdfc266"

OPEN_API_KEY = "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"

pdfreader = PdfReader('C:/Users/Anfinsen/PycharmProjects/Anfinsen/About Me - Anfinsen Joseph.pdf')

from typing_extensions import Concatenate

raw_text = ''
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

llm = OpenAI(openai_api_key=OPEN_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)

astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="harry_db",
    session=None,
    keyspace=None,
)

from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)

texts = text_splitter.split_text(raw_text)

astra_vector_store.add_texts(texts)

# print("Inserted %i headlines." % len(texts))
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

first_question = True
while True:
    if first_question:
        query_text = input("\nEnter your question (or type.'quit'to exit) :. ").strip()
    else:
        query_text = input("\nWhat's your next question (or type 'quit' to exit): ").strip()

    if query_text.lower() == "quit":
        break

    if query_text == "":
        continue

    first_question = False

    print("\nQUESTION: \"%s\"" % query_text)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    print("ANSWER: \"%s\"\n" % answer)

    print("FIRST DOCUMENTS BY RELEVANCE:")
    for doc, score in astra_vector_store.similarity_search_with_score(query_text, k=1):
        print(" [%0.4f] \"%s ... \"" % (score, doc.page_content[:84]))
