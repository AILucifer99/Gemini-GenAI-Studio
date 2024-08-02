import requests
import google.generativeai as genai
import os
import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from dotenv import load_dotenv

load_dotenv()


genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
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

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_loading = "https://lottie.host/cc2b3b2d-5589-4c22-a42b-9c3d50fb8315/b8kIpS7sC0.json"
lottie_loading = load_lottieurl(lottie_url_loading)


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    safety_settings=gemini_safety_settings,
)


def getGeminiResponse(input, image, max_output_tokens=512, tone_of_blog=None) :

    if tone_of_blog == "professional" :
        generation_configuration = {
        "temperature" : 0.75, 
        "top_p" : 0,
        "max_output_tokens" : max_output_tokens, 
        "top_k" : 10, 
        "stop_sequences" : [
            "Thank you for asking me this.", 
            "Thank you."]
        }
        
        if input != "" :
            response = model.generate_content(
                contents=[input, image], 
                generation_config=generation_configuration, 
            )
        else :
            response = model.generate_content(
                contents=image
            )
        
        return response.text 

    elif tone_of_blog == "creative" :
        generation_configuration = {
        "temperature" : 0.95, 
        "top_p" : 0.2,
        "max_output_tokens" : max_output_tokens, 
        "top_k" : 140, 
        "stop_sequences" : [
            "Thank you for asking me this.", 
            "Thank you."]
        }
        
        if input != "" :
            response = model.generate_content(
                contents=[input, image], 
                generation_config=generation_configuration, 
            )
        else :
            response = model.generate_content(
                contents=image
            )
        
        return response.text 

    elif tone_of_blog == "friendly" :
        generation_configuration = {
        "temperature" : 1, 
        "top_p" : 0.2,
        "max_output_tokens" : max_output_tokens, 
        "top_k" : 40, 
        "stop_sequences" : [
            "Thank you for asking me this.", 
            "Thank you."]
        }
        
        if input != "" :
            response = model.generate_content(
                contents=[input, image], 
                generation_config=generation_configuration, 
            )
        else :
            response = model.generate_content(
                contents=image
            )
        
        return response.text 

    elif tone_of_blog == "informative" :
        generation_configuration = {
        "temperature" : 0.75, 
        "top_p" : 0,
        "max_output_tokens" : max_output_tokens, 
        "top_k" : 140, 
        "stop_sequences" : [
            "Thank you for asking me this.", 
            "Thank you."]
        }
        
        if input != "" :
            response = model.generate_content(
                contents=[input, image], 
                generation_config=generation_configuration, 
            )
        else :
            response = model.generate_content(
                contents=image
            )
        
        return response.text 
    
    else :
        generation_configuration = {
        "temperature" : 0.95, 
        "top_p" : 0.2,
        "max_output_tokens" : max_output_tokens, 
        "top_k" : 140, 
        "stop_sequences" : [
            "Thank you for asking me this.", 
            "Thank you."]
        }
        
        if input != "" :
            response = model.generate_content(
                contents=[input, image], 
                generation_config=generation_configuration, 
            )
        else :
            response = model.generate_content(
                contents=image
            )
        
        return response.text 


st.set_page_config(
    page_title="Visual Blog Generation Engine", 
    layout="wide",
    page_icon="🖼️"
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

st.title("Visual *Image to Blog Generation* Engine Powered By *Google Gemini* Large Language Model ✨")
st.subheader("Just upload an image and let Google Gemini create an entire description of the same or you can also generate an entire blog for articles.", divider="rainbow")

uploaded_file = st.file_uploader("Choose an image...", type=["jpeg", "jpg", "png"])
image = ""

if uploaded_file is not None :
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_column_width=False)


input = st.text_input("Enter Your Querry User")

st.sidebar.header("Configuration for the System", divider="rainbow")
tone_of_blog = st.sidebar.radio(
    "Tone Of the Text Generation", 
    options=["Professional", "Creative", "Friendly", "Informative"], 
    horizontal=True,
)

max_output_tokens = st.sidebar.slider("Maximum Output Tokens", 128, 1024, 512, 64)

submit = st.sidebar.button("✨ Generate with Gemini ✨")


if submit :
    st.subheader("Generating The Blog With Tone :- *{}*, Please Wait.....".format(tone_of_blog))
    with st_lottie_spinner(lottie_loading, height=175, width=175, speed=0.75, quality="high") :
        response = getGeminiResponse(
            input=input, image=image, 
            max_output_tokens=max_output_tokens, 
        )

        st.success("Text Extracted From Image Successfully.")
        st.subheader("Gemini Response :-", divider="rainbow")
        container = st.container(border=True, height=None)
        container.write(response)
