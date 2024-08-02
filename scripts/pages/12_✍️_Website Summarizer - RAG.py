import streamlit as st
import os
import validators
import requests
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from langchain_google_genai import ChatGoogleGenerativeAI
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_loading = "https://lottie.host/cc2b3b2d-5589-4c22-a42b-9c3d50fb8315/b8kIpS7sC0.json"
lottie_loading = load_lottieurl(lottie_url_loading)


def GenerateWebsiteSummary(website_url, tone_of_generation, num_words) :
    loader = WebBaseLoader(website_url)
    docs = loader.load()

    if tone_of_generation == "Professional" :

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.45, 
            top_p=0, 
            google_api_key=gemini_api_key, 
            top_k=40, 
            max_output_tokens=num_words,
        )

        # To extract data from WebBaseLoader
        doc_prompt = PromptTemplate.from_template("{page_content}")

        # To query Gemini
        llm_prompt_template = """Write a medium to long form detailed summary using professional english for the following:
        "{text}"
        SUMMARY:"""

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
    
    elif tone_of_generation == "Creative" :
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.75, 
            top_p=0.2, 
            google_api_key=gemini_api_key, 
            top_k=120, 
            max_output_tokens=num_words
        )

        # To extract data from WebBaseLoader
        doc_prompt = PromptTemplate.from_template("{page_content}")

        # To query Gemini
        llm_prompt_template = """Write a medium to long form detailed summary using professional english for the following:
        "{text}"
        SUMMARY:"""

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

    elif tone_of_generation == "Informative" :
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.75, 
            top_p=0.2, 
            google_api_key=gemini_api_key, 
            top_k=120, 
            max_output_tokens=num_words,
        )

        # To extract data from WebBaseLoader
        doc_prompt = PromptTemplate.from_template("{page_content}")

        # To query Gemini
        llm_prompt_template = """Write a medium to long form detailed summary using professional english for the following:
        "{text}"
        SUMMARY:"""

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
    
    else :
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.75, 
            top_p=0, 
            google_api_key=gemini_api_key, 
            top_k=10, 
            max_output_tokens=num_words,
        )

        # To extract data from WebBaseLoader
        doc_prompt = PromptTemplate.from_template("{page_content}")

        # To query Gemini
        llm_prompt_template = """Write a medium to long form detailed summary using professional english for the following:
        "{text}"
        SUMMARY:"""

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
            page_icon="✍️", 
            layout="wide"
        )
        
        st.markdown(
            r"""
            <style>
            .stDeployButton {
                    visibility: hidden;
                }
            </style>
            """, unsafe_allow_html=True
        )

        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        # st.markdown("""
        #     <style>
        #         .stButton button {
        #             background-color: #4CAF50;
        #             color: white;
        #         }
        #     </style>
        # """, unsafe_allow_html=True)

        st.markdown("""
            <style>
                .stButton button {
                    background-color: #000001;
                    color: white;
                }
            </style>
        """, 
        unsafe_allow_html=True)
        
        st.title("RAG System - Automatic *Website Summary Generator* Engine powered by *Google Gemini* Large Language Model ✨")
        st.subheader("Just provide a website url and let Google Gemini Summarize it for you.", divider="rainbow")

        st.sidebar.header("Configuration for the System", divider="rainbow")

        website_url = st.sidebar.text_input("Enter Website URL", "https://medium.com/@kutovenko/flutter-offline-speech-recognition-with-vosk-645791c312fa")
        num_total_words = st.sidebar.slider("Maximum Length Of The Generated Content", 128, 2048, 1024, 1)

        tone_of_generation = st.sidebar.radio(
            "Tone Of The Generation", 
            ["Professional", "Creative", "Informative", "Default"],
            horizontal=True,
        )

        if st.sidebar.button("✨ Generate With Gemini ✨") :
            if not gemini_api_key :
                st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
            elif not validators.url(website_url) :
                st.sidebar.error("Invalid URL. Please enter a valid URL.")
            else :
                st.subheader("Generating The Website Summary With Tone :- {}, Please Wait.....".format(tone_of_generation))
                with st_lottie_spinner(lottie_loading, height=175, width=175, speed=0.75, quality="high") :
                    try :
                        result = GenerateWebsiteSummary(
                            website_url, 
                            tone_of_generation, 
                            num_total_words
                        )
                        st.success("Website Summary Generated Successfully.")
                        st.subheader("Gemini Response :-", divider="rainbow")
                        container = st.container(border=True, height=None)
                        container.write(result)

                    except Exception as exp:
                        st.sidebar.error(f"Error: {str(exp)}")


WebsiteSummarizer(parse_function=True)