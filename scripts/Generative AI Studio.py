import streamlit as st
import os


def validateGeminiAPIKey(input_string):
    # Find the starting index of "AIzaSy"
    start_index = input_string.find("AIzaSy")
    
    if start_index != -1:
        # Extract "AIzaSy" and everything that follows
        extracted_portion = input_string[start_index:6]
        return extracted_portion
    else:
        return None  # Return None if "AIzaSy" is not found in the input string


def HomePage(**kwargs) :
    if kwargs["parse_function"] :
        # Streamlit application
        st.set_page_config(
            page_title="Generative AI Studio", 
            page_icon="🤖", 
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

        st.markdown(
            f'''
                <style>
                    .sidebar .sidebar-content {{
                        width: 1280px;
                    }}
                </style>
            ''',
            unsafe_allow_html=True
        )

        st.write("# The Generative AI Studio powered by Google Gemini! 🤖")

        st.write("##### This application leverages the power of Google's Gemini Model to provide advanced AI services through a user-friendly Streamlit interface. Users can interact with various features designed to enhance productivity and efficiency.{}".format("\n\n"))

        st.header("Features of the Web Application ✨", divider="rainbow")

        st.markdown("""
        ###### 1.   Website Summary Engine ✍️ - Provide any valid website url and let Gemini Summarize the contents for you.
        ###### 2.   Chat with PDF Documents Engine 📜 - Upload any PDF files and start asking questions and let Gemini answer it for you.
        ###### 3.   Automatic Blog Generation Engine 📚 - Just provide a title, some keywords and also other instructions and generate full length blog with Gemini Model.
        ###### 4.   Text Paraphrasing Engine 🖍️ - Copy and paste any english text and let Gemini Paraphrase it for you.
        ###### 5.   Text Summarization Engine ✒️ - Create any type of text summary with the help of Gemini Model. 
        ###### 6.   Automatic Email Generation Engine 📧 - Just provide your email subject and let Gemini write the entire email for you.
        ###### 7.   Automatic Keywords Extraction Engine 📝 - Just provide your text and let Google Gemini generate keywords for you in a very efficient way.
        ###### 8.   Image To Text Generation Engine 🖼️ - Upload an Image and provide a textual guide for the same to generate an entire document out of it. 
        ###### 9.   Q&A Streaming Chat Engine ❓ - Ask any questions and generate the answers using Google Gemini Model. 
        ###### 10.   Code Generation Engine 💡 - Just provide the brief description about the code along with the coding language and let Google Gemini generate the entire code for the same.
        ###### 11.   Code Explaining Engine ⚡ - Provide the entire code and let Google Gemini explain all the details of the code in an excellent way.
        ###### 12.   AI Sentiment Analysis Engine 😁 - Just provide the text and let Google Gemini extract the sentiment of the text.
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
        st.sidebar.image("scripts\\assets\\Googles-Gemini.jpg", use_column_width=True)

        # google_gemini_api_key = st.sidebar.text_input(
        #     "Enter your Google Gemini API Key.", 
        #     type="password"
        # )
        # if google_gemini_api_key is not None and len(google_gemini_api_key) > 10 :
        #     input_str = google_gemini_api_key
        #     extracted = validateGeminiAPIKey(input_str)
        #     if extracted == "AIzaSy" :
        #         st.sidebar.success("Gemini API Key validated successfully.")
        # else :
        #     st.sidebar.warning("Provide Correct Gemini API Key.")
        #     st.sidebar.warning("Try Agin, please...")
            

HomePage(parse_function=True)
