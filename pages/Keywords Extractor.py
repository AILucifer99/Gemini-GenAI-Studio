import streamlit as st
import google.generativeai as genai  
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=gemini_api_key)

st.set_page_config(
    page_title="AI Keywords Extractor Engine",
    layout="wide", 
    page_icon="📑"
)

generation_configuration = {
    "temperature" : 0.75,
    "top_p" : 0.5,
    "max_output_tokens" : 1260, 
    "top_k" : 10,
}

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


gemini_safety_settings = [
    {
        "category" : 'HARM_CATEGORY_HARASSMENT',
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE", 
    }, 
    {
        "category" : "HARM_CATEGORY_HATE_SPEECH", 
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE",
    }, 
    {
        "category" : "HARM_CATEGORY_SEXUALLY_EXPLICIT", 
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category" : "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE",
    }
]


model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_configuration,
    safety_settings=gemini_safety_settings,
)


st.title("Keywords Extractor Engine powered by Google Gemini ✨")

st.subheader(
    "Just provide the engine with a large chunk of text and let Google Gemini extract keywords for you.", 
    divider="rainbow"
)

st.sidebar.header("Configuration for the System", divider="rainbow")

original_text = st.sidebar.text_area("Enter the Text")
num_words = st.sidebar.slider("Number of Keywords (Approximately)", min_value=4, max_value=64, step=16)


if st.sidebar.button("Extract Keywords") :
    if not gemini_api_key:
        st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
    else:
        with st.spinner("Extracting Keywords, please wait.....") :
            try:
                prompt_instruction = [
                    f"You are an excellent blog writer and can analyse blogs with great details. Extract {num_words} comma seperated keywords for the given text \"{original_text}\". Make sure to use professional English tonality. The keywords that you are generating should be always followed by a comma. Keywords can be considered as a single word or a phrase of two to three or maybe four words." 
                ]
                response = model.generate_content(prompt_instruction)
                st.success("Keywords Suggestion by Google Gemini")
                st.write(response.text)
            except Exception as exp :
                st.warning("Error Occured While Generation, please try later.")
                st.write(exp)

