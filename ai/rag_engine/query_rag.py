from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from rag_config import get_openai_api

embeddings = OpenAIEmbeddings(openai_api_key=get_openai_api())
db = FAISS.load_local("faiss_index", embeddings)
llm = ChatOpenAI(temperature=0, openai_api_key=get_openai_api())
qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

while True:
    q = input("Ask: ")
    if q.lower() == 'exit': break
    print(qa.run(q))