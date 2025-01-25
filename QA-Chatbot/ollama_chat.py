from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st

import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING"]="true"
os.environ["LANGCHAIN_PROJECT"]="QA Chatbot WITH Ollama"

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helful assiatant.Please respond to the user queries"),
        ("user","Question: {question}"),
    ]
)

def generate_response(question,llm,temperature,max_tokens):
    llm=Ollama(model=llm)
    output_parser=StrOutputParser()
    chain=prompt | llm | output_parser
    answer=chain.invoke({'question':question})
    return answer

## Title of the app
st.title("Enhanced QA Chatbot")
st.sidebar.title("Settings")
# api_key=st.sidebar.text_input("API Key",type="password")




llm=st.sidebar.selectbox("Select the LLM",["phi3"])
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=500,value=150)

##Main interface

st.write("Go ahead and ask your questions")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input,llm,temperature,max_tokens)
    st.write("Bot:",response)   
else:
    st.write("Bot: Please ask a question")  