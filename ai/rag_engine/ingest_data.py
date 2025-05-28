import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from rag_config import get_openai_api

def ingest():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../face_recognition/metadata.json"))
    data = json.load(open(path))

    docs = [Document(page_content=f"{item['name']} registered at {item['timestamp']}") for item in data]

    embeddings = OpenAIEmbeddings(openai_api_key=get_openai_api())
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")

if __name__ == "__main__":
    ingest()