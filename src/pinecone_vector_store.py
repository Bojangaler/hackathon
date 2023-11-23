import os
from dotenv import load_dotenv
import streamlit as st
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

load_dotenv()

PINCONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENV = os.environ["PINECONE_ENV"]
VECTOR_INDEX_NAME = os.environ["VECTOR_INDEX_NAME"]


@st.cache_resource(show_spinner=False)
def get_retriever():
    # initialize pinecone
    pinecone.init(api_key=PINCONE_API_KEY, environment=PINECONE_ENV)
    embeddings = OpenAIEmbeddings()

    pinecone_client = Pinecone.from_existing_index(VECTOR_INDEX_NAME, embeddings)

    retriever = pinecone_client.as_retriever(search_type="mmr")

    return retriever
