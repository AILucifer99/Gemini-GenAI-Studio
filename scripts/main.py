import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")


def GenerateWebsiteSummary(website_url, temperature, top_p_sampling) :
    loader = WebBaseLoader("{}".format(website_url))
    docs = loader.load()

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=temperature, 
        top_p=top_p_sampling, 
        google_api_key=gemini_api_key
    )


    # To extract data from WebBaseLoader
    doc_prompt = PromptTemplate.from_template("{page_content}")

    # To query Gemini
    llm_prompt_template = """Write a concise summary using professional english for the following:
    "{text}"
    CONCISE SUMMARY:"""

    llm_prompt = PromptTemplate.from_template(llm_prompt_template)

    # Create Stuff documents chain using LCEL.
    # This is called a chain because you are chaining
    # together different elements with the LLM.
    # In the following example, to create stuff chain,
    # you will combine content, prompt, LLM model and
    # output parser together like a chain using LCEL.
    #
    # The chain implements the following pipeline:
    # 1. Extract data from documents and save to variable `text`.
    # 2. This `text` is then passed to the prompt and input variable
    #    in prompt is populated.
    # 3. The prompt is then passed to the LLM (Gemini).
    # 4. Output from the LLM is passed through an output parser
    #    to structure the model response.

    stuff_chain = (
        # Extract data from the documents and add to the key `text`.
        {
            "text": lambda docs: "\n\n".join(
                format_document(doc, doc_prompt) for doc in docs
            )
        }
        | llm_prompt         # Prompt for Gemini
        | llm                # Gemini function
        | StrOutputParser()  # output parser
    )

    website_summary = stuff_chain.invoke(docs)

    return website_summary


result = GenerateWebsiteSummary(
    "https://medium.com/@kutovenko/flutter-offline-speech-recognition-with-vosk-645791c312fa", 
    0.75,
    0.85,
)

print("Result :- {}{}".format("\n", result))
