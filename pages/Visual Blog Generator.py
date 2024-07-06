from dotenv import load_dotenv
load_dotenv()

from PIL import Image
import google.generativeai as genai
import os
import streamlit as st


genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    model_name="gemini-pro-vision"
)


def getGeminiResponse(
        input, image, temperature=0.75, 
        top_p=0, max_output_tokens=512, top_k=1) :
    
    generation_configuration = {
    "temperature" : temperature, 
    "top_p" : top_p,
    "max_output_tokens" : max_output_tokens, 
    "top_k" : top_k, 
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
    page_icon="🎆"
)

st.header("Visual Image to Blog Generation Engine Powered By Google Gemini Model 🎆")

uploaded_file = st.file_uploader("Choose an image...", type=["jpeg", "jpg", "png"])
image = ""
if uploaded_file is not None :
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


input = st.text_input("Enter Your Querry User")
submit = st.button("Ask Gemini")


st.sidebar.header("Configuration For Gemini Output", divider="rainbow")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.3, 0.01)
top_p = st.sidebar.slider("Top_P Sampling", 0.0, 1.0, 0.2, 0.01)
top_k = st.sidebar.slider("Top K Value", 1, 150, 40, 10)
max_output_tokens = st.sidebar.slider("Maximum Output Tokens", 128, 4096, 2048, 128)


if submit :
    with st.spinner("Generation Ongoing, please wait.....") :
        response = getGeminiResponse(
            input=input, image=image, 
            temperature=temperature, 
            top_p=top_p, 
            max_output_tokens=max_output_tokens, 
            top_k=top_k
        )
        st.subheader("Gemini Response :-", divider="rainbow")
        st.success("Output Generated")
        st.write(response)



