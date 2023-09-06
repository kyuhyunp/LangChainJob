import streamlit
import langchain_helper

CONVERSATION_QS = ["What day did I apply?", "What company did I apply to?", "What position did I apply for?"]
AGENT_QS = ["What is the URL address of the company?"]


streamlit.title("Job Helper")

documents = langchain_helper.get_documents()
memory = langchain_helper.get_memory()
conversation_chain = langchain_helper.get_conversational_retrieval_chain(documents, memory)
for query in CONVERSATION_QS:
    streamlit.write(query)
    answer = langchain_helper.get_conversation_answer(conversation_chain, query)
    streamlit.write(answer)

agent_chain = langchain_helper.get_agent_chain(memory)
for query in AGENT_QS:
    streamlit.write(query)
    answer = langchain_helper.get_agent_answer(agent_chain, query)
    streamlit.write(answer)
