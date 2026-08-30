import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
def format_documents(documents):

    return "\n\n".join(
        document.page_content
        for document in documents
    )


def create_qa_chain():

    prompt = ChatPromptTemplate.from_template(
        """
        You are a document question-answering assistant.

        Answer the user's question using ONLY the context
        provided below.

        If the answer cannot be found in the context,
        say:

        "I don't know based on the provided documents."

        Do not make up information.

        Context:
        {context}

        Question:
        {question}
        """
    )


    model = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


    parser = StrOutputParser()


    chain = prompt | model | parser


    return chain






