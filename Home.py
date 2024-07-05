import streamlit as st
import os


def HomePage(**kwargs) :
    if kwargs["parse_function"] :
        # Streamlit application
        st.set_page_config(
            page_title="Gemini AI Studio", 
            page_icon="✨", 
            layout="wide"
        )

        # st.sidebar.image("assets\\Gemini-Logo.jpg")

        st.markdown("""
            <style>
                .stButton button {
                    background-color: #4CAF50;
                    color: white;
                }
            </style>
        """, 
        unsafe_allow_html=True
        )

        st.write("# Welcome to the AI Studio powered by Google Gemini! 👋")

        st.write("##### This application leverages the power of Google's Gemini Model to provide advanced AI services through a user-friendly Streamlit interface. Users can interact with various features designed to enhance productivity and efficiency.{}".format("\n\n"))

        st.header("Features of the Web Application ✨", divider="rainbow")

        st.markdown("""
        ###### 1.   Website Summaries - Provide any valid website url and let Gemini Summarize the contents for you.
        ###### 2.   Chat with PDF Documents - Upload any PDF files and start asking questions and let Gemini answer it for you.
        ###### 3.   Generate English Blogs - Just provide a title, some keywords and also other instructions and generate full length blog with Gemini Model.
        ###### 4.   Paraphrase Text - Copy and paste any english text and let Gemini Paraphrase it for you.
        ###### 5.   Summarize Text - Create any type of text summary with the help of Gemini Model. 
        ###### 6.   Email Generation Engine - Just provide your email subject and let Gemini write the entire email for you.
        """
        )

        st.header("Configuration Details", divider="rainbow")
        st.markdown("""
        ###### 1.   Temperature - The sampling temperature for text generation affects how predictable the output is; higher values make it less predictable. Avoid adjusting both temperature and top_p simultaneously.
        ###### 2.   Top P Sampling - The top-p sampling mass for text generation determines the probability mass considered. For example, with top_p = 0.2, only tokens with a cumulative probability of 0.2 are sampled. Avoid adjusting both temperature and top_p simultaneously.
        ###### 3.   Max New Tokens - The maximum number of tokens to generate in a single call. The model will stop generating when it reaches this limit.
        """
        )

        st.sidebar.success("Select a feature for use.")


HomePage(parse_function=True)

