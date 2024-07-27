import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
from hugchat import hugchat
from hugchat.login import Login

# Load environment variables
load_dotenv()

# Define the local path to the PDF file
PDF_PATH = "./pdf_folder/jaybiodatalatest_ver2.0.pdf"

# Define a function to read the PDF content
def read_pdf(file_path):
    reader = PdfReader(file_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content

# Login to HuggingChat
EMAIL = os.getenv("HUGGINGCHAT_EMAIL")
PASSWD = os.getenv("HUGGINGCHAT_PASSWORD")
cookie_path_dir = "./cookies/"
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

# Create the ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

# Read PDF content from the local path
pdf_content = read_pdf(PDF_PATH)

# Streamlit UI
st.title("PDF-based Chatbot")

# Input for the question
question = st.text_input("Ask a question")

if st.button("Get Answer"):
    if question:
        # Get the answer from the PDF content
        answer = chatbot.chat(f"{pdf_content}\n\nQuestion: {question}")
        st.write("Answer:", answer.wait_until_done())
    else:
        st.write("Please enter a question.")
