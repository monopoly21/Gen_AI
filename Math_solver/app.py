import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain,LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="Text To Math Solver",page_icon="🧮",layout="centered",initial_sidebar_state="expanded")
st.title("Text To Math Solver Using Google Gemma 2")

groq_api_key=st.sidebar.text_input("Enter your GROQ API Key",type="password")

if not groq_api_key:
    st.info("Please enter your GROQ API Key")
    st.stop()   

llm=ChatGroq(model="Llama3-8b-8192",groq_api_key=groq_api_key)

# Initializing tools

wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="Get information from Wikipedia to find various info on topic",
)


# Initalize math Tool

math_chain=LLMMathChain.from_llm(llm=llm)

calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="Calculate the math expression.Only input the math expression",
)


prompt="""
    you are a agent taksed for solving mathemathical problems.Logicallly solve the following math problem:
    Question:{question}
    Answer:
"""

prompt_template=PromptTemplate(template=prompt,input_variables=["question"])


# Combine all the tools into chain 
chain=LLMChain(llm=llm,prompt=prompt_template)


reasoning_tool=Tool(
    name="Reasoning Tool",
    func=chain.run,
    description="tool for solving logic-based and reasoning questions"
)


assistant_agent=initialize_agent(
    tools=[wikipedia,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_erros=True,
)

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi! I am a Math Chatbot. I can help you with math problems. Please ask me a question."}
    ]


for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])


# Function to generate response 

def generate_response(question:str):
    response=assistant_agent.invoke({"input":question})
    return response


# Lets start the interaction with the chatbot. Ask me a math question.

question=st.text_input("Ask me a math question")    

if st.button("Find my Answer"):
    if question:
        with st.spinner("Thinking..."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)

            respone=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write("### Response:")
            st.success(response)
    else:
        st.warning("Please ask me a question")
