## AI Lingualistic Hub Powered by Google Gemini Multi-Modal Large Language Model.

An implementation of end to end AI lingualistic ecosystem with Google Gemini Model. The project deals with many features like AI Blog Generation, AI Text Summarization, Paraphrasing and many more. The entire system is using Google Gemini Large Language Model to solve the respective tasks. 

### Application Home Page
![Gemini Multilingual Studio](https://github.com/AILucifer99/Gemini-Multilingual-Studio/blob/main/scripts/assets/Application.png?raw=true)

### Usage Guidelines
For using the system, follows the below provided steps one after the other in a sequential manner. 
1.   Generate a Google API Key from the website - `https://aistudio.google.com/app/apikey`
2.   Once the API key is generated, save it in a file.
3.   Clone the repository by the command - `git clone https://github.com/AILucifer99/Gemini-Multilingual-Studio`
4.   Once the repository cloning is done, copy the API key from the file and create another file named as `.env`, and save it there.
5.   Move the `.env` to the project root folder
6.   Open the command prompt and create the Python virtual enviorenment.
7.   Once enviorenment is created, run the command - `pip install -r requirements.txt`
8.   Run the command - `streamlit run "Gemini MultiLingual Studio.py"`
9.   The application will be running on the URL - `http://localhost:8501`
10.   Start using the application and unleash the power of the Google Gemini Large Language MultiModal Model.

### Parameters in the GUI
The system is designed in such a way that an end user can control the generation of the Gemini Large Language Model. So, many parameters are also provided in the GUI for the controlling. The parameters are consistent throughout the GUI. 
1.   Temperature - The sampling temperature for text generation affects how predictable the output is; higher values make it less predictable. Avoid adjusting both temperature and top_p simultaneously.
2.   Top P Sampling - The top-p sampling mass for text generation determines the probability mass considered. For example, with top_p = 0.2, only tokens with a cumulative probability of 0.2 are sampled. Avoid adjusting both temperature and top_p simultaneously.
3.   Max New Tokens - The maximum number of tokens to generate in a single call. The model will stop generating when it reaches this limit.

#### These three parameters are the main controlling components of the Gemini Model, so tuning these values can help a lot in generating variety of outputs for the same prompt and thus, the generation can be much more relieable and robust. 
