from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from typing import List, Dict
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def load_vdb_and_retriever(path="defi_e_mf",
                           k=4):
    embedding_size = 1536
    embedding_model = "text-embedding-3-small"
    embeddings = OpenAIEmbeddings(model=embedding_model, dimensions=embedding_size)
    
    vdb = FAISS.load_local(path, 
                           embeddings, 
                           allow_dangerous_deserialization=True)
    
    retriever = vdb.as_retriever(search_kwargs={"k": k})
    
    return vdb, retriever

def response(input):
    vdb, retriever = load_vdb_and_retriever()

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    system_prompt = """
    Você é um assistente de IA que vai tirar dúvidas sobre finanças descentralizadas e mercado financeiro. 

    Além disso, aqui está um conteudo extra sobre finanças descentralizadas e/ou mercado financeiro:

    [Conteudo extra]
    {extra_content}
    [Final do conteudo extra]

    --------------------------------------------
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    chain = (
    {
        "input" : itemgetter("input"),
        "extra_content": itemgetter("input") | retriever | RunnableLambda(format_docs)
    }
    | prompt
    | llm
    | StrOutputParser()
    )
    return chain.stream({"input": input})

def format_docs(docs: List[Document]) -> str:
    return "\n".join([x.page_content for x in docs])


