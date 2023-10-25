import os, sys

from constants import openapi_key
from constants import serpapi_key

from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.vectorstores import Chroma
from langchain.agents import AgentType, initialize_agent, load_tools


__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ['OPENAI_API_KEY'] = openapi_key
os.environ['SERPAPI_API_KEY'] = serpapi_key


def generate_job_log(texts):
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={'k': 1}))
    
    job = {}
    job["employerName"] = qa.run("What company did I apply to? Output just the direct single answer").strip()
    job["date"] = qa.run(f"What date did I apply to {job['employerName']} in MM-DD-YYYY format? Output just the direct single answer").strip()
    job["jobTitle"] = qa.run(f"For what job position did I apply to {job['employerName']}? Output just the direct single answer").strip()

    print(job)
    return job


def searchURL(company):
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent.run(f"Find the url of the company : {company} excluding anything else but the url")
    
