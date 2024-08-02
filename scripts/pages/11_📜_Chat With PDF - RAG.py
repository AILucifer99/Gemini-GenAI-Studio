import streamlit as st
import os
import google.generativeai as genai
import requests

from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_loading = "https://lottie.host/cc2b3b2d-5589-4c22-a42b-9c3d50fb8315/b8kIpS7sC0.json"
lottie_loading = load_lottieurl(lottie_url_loading)


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0.3, 
        max_output_tokens=2048, 
        top_k=40
    )

    prompt = PromptTemplate(
        template = prompt_template, 
        input_variables = ["context", "question"]
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local(
        "faiss_index", embeddings, 
        allow_dangerous_deserialization=True
    )
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.success("Gemini Generated Successfully...")
    st.subheader("Gemini Response for the question", divider="rainbow")
    container = st.container(border=True, height=None)
    container.write(response.text)


def main():
    st.set_page_config(
        "Chat With PDF Engine", 
        layout="wide", 
        page_icon="📜"
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
    #         <style>
    #             .stButton button {
    #                 background-color: #4CAF50;
    #                 color: white;
    #             }
    #         </style>
    #     """, 
    # unsafe_allow_html=True
    # )

    st.markdown("""
            <style>
                .stButton button {
                    background-color: #000001;
                    color: white;
                }
            </style>
        """, 
    unsafe_allow_html=True, )
    st.title("RAG System - Multiple PDF Documents *Question and Answering Engine* powered by *Google Gemini* Large Language Model ✨")
    st.subheader("Upload multiple PDF files to the engine and let Google Gemini answer any questions from the same.", divider="rainbow")
 
    user_question = st.text_input("Ask a Question from the PDF Files")
    question_button = st.button("✨ Generate With Gemini ✨")

    if user_question :
        if question_button :
            st.subheader("Generating The Answer, please wait.....")
            with st_lottie_spinner(lottie_loading, height=175, width=175, speed=0.75, quality="high") :
                user_input(user_question)


    with st.sidebar :
        st.header("Configuration of the System.", divider="rainbow")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button", 
            accept_multiple_files=True
        )
        if st.button("✨ Preprocess Data With Gemini ✨") :
            with st.spinner("Generating Embeddings, please wait....") :
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


main()