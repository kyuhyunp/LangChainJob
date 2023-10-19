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
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


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
    Answer the following questions with one word response as best you can.
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

def get_conversation_answer(conversational_chain, query: str):
    result = conversational_chain({"question": query})

    return result["answer"]

def get_agent_chain(memory):
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi"], llm=llm)

    prefix = """Have a conversation with a human, answering the following questions with one word response as best you can. You have access to the following tools:"""
    suffix = """Begin!"

    {chat_history}
    Question: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "chat_history", "agent_scratchpad"],
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
    return AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True, memory=memory
    )

def get_agent_answer(agent_chain, query: str):
    result = agent_chain.run(query)
    return result
