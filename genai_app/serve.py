from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

system_template="Translate the following into {langauage}:"

prompt=ChatPromptTemplate.from_messages(
    [("system",system_template),("user","text")]
)


parser=StrOutputParser()

chain=prompt|model|parser



app=FastAPI(title="Langchain Server 0.1",description="This is a server for langchain",version="0.1")

add_routes(app,chain,path="/chain")

if __name__ == "main":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port="3000 ")