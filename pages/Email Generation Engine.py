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
    page_title="Automatic Email Generation Engine",
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


st.title("Generate outstanding emails with Email Generation Engine powered by Google Gemini ✨")

st.subheader(
    "Just provide the engine with an *email subject text* and let *Google Gemini* write the entire mail for you.", 
    divider="rainbow"
)

st.sidebar.header("Configuration for the System", divider="rainbow")

original_text = st.sidebar.text_area("Enter the Subject For The Mail")
num_words = st.sidebar.slider("Number of words in the mail (Approximately)", min_value=50, max_value=500, step=2)
temperature = st.sidebar.slider("Degree Of Creativeness", min_value=0.0, max_value=2.0, step=0.01)


if st.sidebar.button("Generate Email") :
    if not gemini_api_key:
        st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
    else:
        with st.spinner("Generation of Email is ongoing, please wait.....") :
            try:
                prompt_instruction = [
                    f"You are an excellent email writer where you need only the subject to generate the mail. Therefore, generate an email with approximately {num_words} words for the provided subject text \"{original_text}\". Make sure to use professional English tonality. If no details for the mail recipients are provided, then just leave blank spaces for the same in the generated email." 
                ]
                response = model.generate_content(
                    prompt_instruction, 
                    generation_config={
                        "temperature" : temperature, 
                        }
                    )
                st.success("Gemini Generation Successfully completed.")
                st.subheader("Gemini Generated Email", divider="rainbow")
                st.write(response.text)
            except Exception as exp :
                st.warning("Error Occured While Generation, please try later.")
                st.write(exp)

