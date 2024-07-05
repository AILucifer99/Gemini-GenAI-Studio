import streamlit as st
import google.generativeai as genai  
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=gemini_api_key)

st.set_page_config(
    page_title="AI Blog Generator",
    layout="wide", 
    page_icon="📚"
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


st.title("AI SEO Optimized Blog Generator ✨")
st.subheader(
    "Just provide a *blog title*, along with important *keywords* and \
    let Google Gemini generate a blog for the same.", 
    divider="rainbow"
)

st.sidebar.header("Configuration for the System", divider="rainbow")

blog_title = st.sidebar.text_area("Enter the Title of the Blog", "The impact of AI on HealthCare Industries.")
keywords = st.sidebar.text_area("Keywords (Comma-Seperated)", "Artificial Intelligence, Health Care with AI, Automatic Decision for doctors.")
num_words = st.sidebar.slider("Number of tokens", min_value=250, max_value=1500, step=50)


if st.sidebar.button("Generate Blog"):
    if not gemini_api_key:
        st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
    else:
        with st.spinner("Generating the blog, please wait.....") :
            try:
                prompt_instruction = [
                    f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" and keywords \"{keywords}\". Make sure to incorporate these keywords in the blog post. The blog should be approximately {num_words} words." 
                ]
                response = model.generate_content(prompt_instruction)
                st.success("Gemini Generated AI Blog")
                st.write(response.text)
            except Exception as exp :
                st.warning("Error Occured While Generation, please try later.")
                st.write(exp)
