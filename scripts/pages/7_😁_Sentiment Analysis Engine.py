import streamlit as st
import os
import google.generativeai as genai  
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
    page_title="AI Sentiment Analysis Engine",
    layout="wide", 
    page_icon="😁"
)

generation_configuration = {
    "temperature" : 0.75,
    "top_p" : 0.5,
    "max_output_tokens" : 1260, 
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


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_configuration,
    safety_settings=gemini_safety_settings,
)


st.title("Automatic *Textual Sentiment Analysis* Engine powered by *Google Gemini* Large Langauge Model ✨")
st.subheader(
    "Just provide the engine with a large chunk of text and let Google Gemini provide a sentiment analysis for you.", 
    divider="rainbow"
)

st.sidebar.header("Configuration for the System", divider="rainbow")

original_text = st.sidebar.text_area("Enter the Text For Sentiment Analysis")


if st.sidebar.button("✨ Generate With Gemini ✨") :
    if not gemini_api_key :
        st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
    else:
        st.subheader("Generating The Sentiment, Please Wait.....")
        with st_lottie_spinner(lottie_loading, height=175, width=175, speed=0.75, quality="high") :
            try:
                prompt_instruction = [
                    f"You are an awesome researcher working in the domain of English and you are quite good enough to extract the sentiment from a given text. If you think that the text is about something positive, then output Sentiment is Positive, else Sentiment is Negative. If you think that the text is neither positive nor negative, then just say Sentiment is Neutral. So, try to generate the sentiment for the given text \"{original_text}\"" 
                ]
                response = model.generate_content(prompt_instruction)

                st.success("Text Sentiment Extracted Successfully.")
                st.subheader("Gemini Response :-", divider="rainbow")
                container = st.container(border=True, height=None)
                container.write(response.text)

            except Exception as exp :
                st.warning("Error Occured While Generation, please try later.")
                st.write(exp)
