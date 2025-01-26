import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

st.set_page_config(page_title="LangChain: Summarize Text from YT or Website",page_icon="📺",layout="centered",initial_sidebar_state="expanded")
st.title("Summarize Text from Youtube or Website")
st.subheader('Summarize URL')

with st.sidebar:
    groq_api_key = st.text_input("Enter your GROQ API Key",type="password")

generic_url=st.text_input("Enter URL",label_visibility="collapsed")

llm=ChatGroq(model="Llama3-8b-8192",api_key=groq_api_key)

prompt_template="""
    Provide a summary of the content in 300 words
    Content:{text}
"""

prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize The Content From YT or Website"):
    # Validate all inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please fill in all the fields")
    elif not validators.url(generic_url):
        st.error("Invalid URL")
    else:
        try:
            with st.spinner("Waiting..."):
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url,add_video_info=False)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                   headers={"User-Agent":"Mozilla/5.0 ; Windows NT 10.0 ; Win64 ; x64; rv:89.0 ; Gecko/20100101 Firefox/89.0"})
                docs=loader.load()

                # Chain for summarization
                chain =load_summarize_chain(llm=llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)
                st.success(output_summary)
        except Exception as e:
            st.exception(f"An error occurred: {e}")