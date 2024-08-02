import streamlit as st
import google.generativeai as genai  
import os
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from dotenv import load_dotenv
import requests


# Load environment variables
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


st.set_page_config(
    page_title="AI Keywords Extractor Engine",
    layout="wide", 
    page_icon="📝"
)

generation_configuration = {
    "temperature" : 0.75,
    "top_p" : 0.5,
    "max_output_tokens" : 1024, 
    "top_k" : 10,
}

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
#             <style>
#                 .stButton button {
#                     background-color: #4CAF50;
#                     color: white;
#                 }
#             </style>
#         """, 
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
unsafe_allow_html=True
)


gemini_safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


# gemini_safety_settings = [
#     {
#         "category" : 'HARM_CATEGORY_HARASSMENT',
#         "threshold" : "BLOCK_MEDIUM_AND_ABOVE", 
#     }, 
#     {
#         "category" : "HARM_CATEGORY_HATE_SPEECH", 
#         "threshold" : "BLOCK_MEDIUM_AND_ABOVE",
#     }, 
#     {
#         "category" : "HARM_CATEGORY_SEXUALLY_EXPLICIT", 
#         "threshold" : "BLOCK_MEDIUM_AND_ABOVE",
#     },
#     {
#         "category" : "HARM_CATEGORY_DANGEROUS_CONTENT",
#         "threshold" : "BLOCK_MEDIUM_AND_ABOVE",
#     }
# ]


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_configuration,
    safety_settings=gemini_safety_settings,
)


st.title("SEO Optimized *Keywords Extractor* Engine powered by *Google Gemini* Large Language Model ✨")

st.subheader(
    "Just provide the engine with a large chunk of text and let Google Gemini extract search engine optimized keywords for you.", 
    divider="rainbow"
)

st.sidebar.header("Configuration for the System", divider="rainbow")

original_text = st.sidebar.text_area("Enter the Text")
num_words = st.sidebar.slider("Number of Keywords (Approximately)", min_value=4, max_value=64, step=16)


if st.sidebar.button("✨ Generate With Gemini ✨") :
    if not gemini_api_key:
        st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
    else:
        st.subheader("Extracting *{} Keywords* From The Provided Text, Please Wait.....".format(num_words))
        with st_lottie_spinner(lottie_loading, height=175, width=175, speed=0.75, quality="high") :
            try:
                prompt_instruction = [
                    f"You are an excellent blog writer and can analyse blogs with great details as well understand what is Search Engine Optimization. You will extract {num_words} comma seperated search engine optimized keywords for the given text \"{original_text}\". Make sure to use professional English tonality. The keywords that you are generating should be always followed by a comma. Keywords can be considered as a single word or a phrase of two to three or maybe four words." 
                ]
                response = model.generate_content(prompt_instruction)
                
                st.success("Keywords Extracted Successfully.")
                st.subheader("Gemini Response :-", divider="rainbow")
                container = st.container(border=True, height=None)
                container.write(response.text)

            except Exception as exp :
                st.warning("Error Occured While Generation, please try later.")
                st.write(exp)
