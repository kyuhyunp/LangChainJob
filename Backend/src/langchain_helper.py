import os, sys

from constants import openapi_key
from constants import serpapi_key

from langchain import LLMChain
from langchain.agents import load_tools, AgentExecutor, ZeroShotAgent
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader
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


def get_memory():
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def get_conversational_retrieval_chain(documents, memory):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)
    
    general_system_template = """ 
    Answer the following questions as best you can.
    ---
    {context}
    ---
    """
    general_user_template = "```{question}```"
    messages = [
                SystemMessagePromptTemplate.from_template(general_system_template),
                HumanMessagePromptTemplate.from_template(general_user_template)
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)

    return ConversationalRetrievalChain.from_llm(
        OpenAI(temperature=0), 
        vectorstore.as_retriever(search_kwargs={"k": 1}), 
        memory=memory, 
        combine_docs_chain_kwargs={'prompt': qa_prompt})

def get_conversation_answer(conversational_chain):
    result = conversational_chain({"question": """generate a json format with 
                                   keys "date" in MM-DD-YYYY format, "employerName", "jobTitle", and values 
    corresponding to the job I applied to."""})

    return result["answer"]

def searchURL(company):
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent.run(f"Find the url of the company : {company} excluding anything else but the url")
    
