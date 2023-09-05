from constants import openapi_key
from constants import serpapi_key
from langchain import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent, load_tools, AgentExecutor, ZeroShotAgent

import os, sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ['OPENAI_API_KEY'] = openapi_key
os.environ['SERPAPI_API_KEY'] = serpapi_key
#llm = OpenAI(temperature=0.7)
loader = PyPDFLoader("Data/email.pdf")
documents = loader.load_and_split()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vectorstore.as_retriever(search_kwargs={"k": 1}), memory=memory)

query = "What day did I apply?"
result = qa({"question": query})
print(result["answer"])

query = "What company did I apply to?"
result = qa({"question": query})
print(result["answer"])

query = "What position did I apply for?"
result = qa({"question": query})
print(result["answer"])

# Need to use agent
query = "What is the address of the company?"
result = qa({"question": query})
print(result["answer"])

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi"], llm=llm)

## Use agent chain for memory
prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
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
# Research into different agents
llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)
print(agent_chain.run("What is the URL address of the company?"))



