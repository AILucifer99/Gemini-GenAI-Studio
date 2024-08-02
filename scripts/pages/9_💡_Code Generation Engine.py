import streamlit as st
import google.generativeai as genai  
from dotenv import load_dotenv
import os
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
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
    page_title="Code Generation Engine",
    layout="wide", 
    page_icon="💡"
)


generation_configuration = {
    "temperature" : 0.75,
    "top_p" : 0.5,
    "max_output_tokens" : 2048, 
    "top_k" : 40,
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


st.title("Generate any programming code with the *Code Generation Engine* powered by *Google Gemini* Large Language Model ✨")

st.subheader(
    "Just provide the engine with a small description about the code and let Google Gemini guide you through the code.", 
    divider="rainbow"
)

st.sidebar.header("Configuration for the System", divider="rainbow")

original_text = st.sidebar.text_area("Enter the Coding Topic")
temperature = st.sidebar.slider(
    "Degree Of Creativeness", 
    min_value=0.0, max_value=2.0, 
    value=0.75, step=0.01
)

coding_language = st.sidebar.radio(
    "The Coding Language For Gemini",
    [
        "Java", "JavaScript", "Python",
        "C#", "C++", "Rust", "Go", 
        "NodeJS", "ReactJS", "AngularJS"
    ], 
    horizontal=False,
)


if st.sidebar.button("✨ Generate With Gemini ✨") :
    if not gemini_api_key:
        st.sidebar.error("Google API Key is not set. Please set it in the environment variables.")
    else:
        st.subheader("Generating The Code In Language :- *{}*, Please Wait.....".format(coding_language))
        with st_lottie_spinner(lottie_loading, height=175, width=175, speed=0.75, quality="high") :
            try:
                prompt_instruction = [
                    f"""You are not only an excellent coding assistant but also you can write optimized code just from a basic description text that tells about the code's working. 
                    Therefore, generate a code for the provided description text \"{original_text}\" using the coding langauge \"{coding_language}\". Make sure to maintain proper guidelines while generating the code for the user. 
                    If you cannot generate the code then simply say "Can't Generate", do not write the wrong code for the user."""
                ]
                response = model.generate_content(
                    prompt_instruction, 
                    generation_config={
                        "temperature" : temperature, 
                        }
                    )
                st.success("Code Generated Successfully.")
                st.subheader("Gemini Response :-", divider="rainbow")
                container = st.container(border=True, height=None)
                container.write(response.text)

            except Exception as exp :
                st.warning("Error Occured While Generation, please try later.")
                st.write(exp)

