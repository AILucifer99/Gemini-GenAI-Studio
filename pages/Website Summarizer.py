import streamlit as st
import os
import validators
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")


def GenerateWebsiteSummary(website_url, temperature, top_p_sampling, top_k):
    loader = WebBaseLoader(website_url)
    docs = loader.load()

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=temperature, 
        top_p=top_p_sampling, 
        google_api_key=gemini_api_key, 
        top_k=top_k
    )

    # To extract data from WebBaseLoader
    doc_prompt = PromptTemplate.from_template("{page_content}")

    # To query Gemini
    llm_prompt_template = """Write a medium to long form summary using professional english for the following:
    "{text}"
    CONCISE SUMMARY:"""

    llm_prompt = PromptTemplate.from_template(llm_prompt_template)

    stuff_chain = (
        {
            "text": lambda docs: "\n\n".join(
                format_document(doc, doc_prompt) for doc in docs
            )
        }
        | llm_prompt         # Prompt for Gemini
        | llm                # Gemini function
        | StrOutputParser()  # output parser
    )

    website_summary = stuff_chain.invoke(docs)
    return website_summary


def WebsiteSummarizer(**kwargs) :
    if kwargs["parse_function"] :
        # Streamlit application
        st.set_page_config(
            page_title="Website Summary Generator", 
            page_icon="📝", 
            layout="wide"
        )

        st.markdown("""
            <style>
                .stButton button {
                    background-color: #4CAF50;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)

        st.title("Website Summary Generator 📝")
        st.subheader("Just provide a website url and let Google Gemini Summarize it for you.", divider="rainbow")

        st.sidebar.header("Configuration for the System", divider="rainbow")

        website_url = st.sidebar.text_input("Enter Website URL", "https://medium.com/@kutovenko/flutter-offline-speech-recognition-with-vosk-645791c312fa")
        temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.75)
        top_p_sampling = st.sidebar.slider("Top P Sampling", 0.0, 1.0, 0.0)
        top_k = st.sidebar.slider("Top K", 0.0, 150.0, 40.0)

        summary_format = st.sidebar.selectbox("Summary Format", ["Concise", "Detailed"])

        if st.sidebar.button("Generate Summary"):
            if not gemini_api_key:
                st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
            elif not validators.url(website_url):
                st.sidebar.error("Invalid URL. Please enter a valid URL.")
            else:
                with st.spinner("Generating summary..."):
                    try:
                        result = GenerateWebsiteSummary(website_url, temperature, top_p_sampling, top_k)
                        st.sidebar.success("Summary generated successfully!")
                        st.subheader("Gemini Result for the Website", divider="rainbow")
                        st.write("Summary", result, height=300, width=300)
                    except Exception as e:
                        st.sidebar.error(f"Error: {str(e)}")


WebsiteSummarizer(parse_function=True)