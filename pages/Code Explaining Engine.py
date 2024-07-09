import streamlit as st
import google.generativeai as genai  
from dotenv import load_dotenv
import os
from authorization import authorization as auth 


# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
gemini_api_key = auth.GOOGLE_API_KEY


genai.configure(api_key=gemini_api_key)

st.set_page_config(
    page_title="Code Explaining Engine",
    layout="wide", 
    page_icon="📑"
)


generation_configuration = {
    "temperature" : 0.75,
    "top_p" : 0.5,
    "max_output_tokens" : 1024, 
    "top_k" : 40,
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


st.title("Generate code explanations with the Code Explaining Engine powered by Google Gemini ✨")

st.subheader(
    "Just provide the engine with the entire *code* and let *Google Gemini* explain you the code.", 
    divider="rainbow"
)

st.sidebar.header("Configuration for the System", divider="rainbow")

original_text = st.text_area("Enter the Code")
temperature = st.sidebar.slider("Degree Of Creativeness", min_value=0.0, max_value=2.0, step=0.01)
coding_language = st.sidebar.radio(
    "The Coding Language For Gemini",
    [
        "Java", "JavaScript", "Python",
        "C#", "C++", "Rust", "Go", 
        "NodeJS", "ReactJS", "AngularJS"
    ],
)

if st.sidebar.button("Explain the Code") :
    if not gemini_api_key:
        st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
    else:
        with st.spinner("Generation ongoing, please wait.....") :
            try:
                prompt_instruction = [
                    f"""You are not only an excellent coding assistant but also you can explain code just like a coding teacher. 
                    Therefore, generate a detailed explanation for the provided code \"{original_text}\" writen using the \"{coding_language}\" coding language. 
                    Make sure to maintain proper guidelines while generating the code description for the user. 
                    If you cannot generate the code description then simply say "Can't Generate", do not write the wrong code description for the user."""
                ]
                response = model.generate_content(
                    prompt_instruction, 
                    generation_config={
                        "temperature" : temperature, 
                        }
                    )
                st.success("Gemini Generation Successfully completed.")
                st.subheader("Gemini Generated Description of the Code", divider="rainbow")
                st.write(response.text)
            except Exception as exp :
                st.warning("Error Occured While Generation, please try later.")
                st.write(exp)

