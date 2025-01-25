import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv

##Arxiv and Wikipedia Tools
arxiw_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiw_wrapper)
wikepedia=WikipediaQueryRun(api_wrapper=wiki_wrapper)

search=DuckDuckGoSearchRun(name="Search")


st.title("Search Engine")
"""
We are using StreamlitCallbackHandler to see what the thought and actions of the agent are.
"""



st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your GROQ API Key",type="password")


if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {
            "role":"assistant",
            "content":"Hi, I am a Chatbot who can search the web for you. How can I help you today?"
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt:=st.chat_input(placeholder="What is machine learning?") and api_key:
    st.session_state["messages"].append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    llm=ChatGroq(groq_api_key=api_key,model_name="LLama3-8b-8192")
    tools=[arxiv,wikepedia,search]
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_erros=True)

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state["messages"].append({"role":"assistant","content":response["answer"]})
        st.write(response["answer"])