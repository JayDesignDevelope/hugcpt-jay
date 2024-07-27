import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
from hugchat import hugchat
from hugchat.login import Login
import time

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

# Streamlit UI configuration
st.set_page_config(page_title="JayGPT", page_icon=":robot_face:", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .h1{
    color:black;
    }
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 5px;
        margin: 5px;
        width: 100%;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: black;
        padding: 10px;
        border-radius: 5px;
    }
    .message {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        color: black;
    }
    .bot-response {
        color: black;
    }
    .user-query {
        color: black;
    }
    .question-input {
        position: fixed;
        bottom: 0;
        width: 100%;
        padding: 10px;
        background-color: #f0f2f6;
        border-top: 1px solid #ddd;
    }
    .question-input > div {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .question-input .input-text {
        flex: 1;
    }
    .question-input .send-button {
        margin-left: 10px;
        background-color: #1a73e8;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
    }
    .question-input .send-button:hover {
    background-color: grey;
            border: none;

    }

    .card-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
                    border: none;

    }
    .card {
        background-color: #1a73e8;
        color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        cursor: pointer;
        text-align: center;
        width: 200px;
        
    }
    .card:hover {
    background-color: grey;
            border: none;

    }
    
    h1:hover, h2:hover, h3:hover, h4:hover, h5:hover, h6:hover .card .card-container .send-butto{{
            color: black !important;
        }}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <img src="https://avatars.githubusercontent.com/u/69631?v=4" style="border-radius: 50%; width: 100px;"/>
        <h1 style="color: black;">JayGPT</h1>
        <p style="color: black;">My name is JayGPT, here to assist you about Jay.<br>You can ask me anything about Jay professionally.</p>
    </div>
""", unsafe_allow_html=True)

# Pre-defined buttons for quick questions in a single row with a squared shape
quick_questions = [
    ("Where did Jay complete his education?", ""),
    ("What professional certifications does Jay hold?", ""),
    ("What programming languages does Jay know?", ""),
    ("What research has Jay published?", "")
]

st.markdown("<div class='card-container'>", unsafe_allow_html=True)
for q, subtext in quick_questions:
    if st.button(q):
        st.session_state["last_question"] = q
        with st.spinner("Generating answer..."):
            answer = chatbot.chat(f"{pdf_content}\n\nQuestion: {q}")
            st.session_state["last_answer"] = answer.wait_until_done()
        st.experimental_rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Function to create typing effect
def typing_effect(text):
    result = ""
    for char in text:
        result += char
        st.markdown(f"<div class='bot-response'>{result}</div>", unsafe_allow_html=True)
        time.sleep(0.05)

# Display the current question and answer
if "last_question" in st.session_state and "last_answer" in st.session_state:
    st.markdown(f"<div class='message'><b class='user-query'>Question:</b> {st.session_state['last_question']}<br><b class='bot-response'>Answer:</b> {st.session_state['last_answer']}</div>", unsafe_allow_html=True)

# Fixed input box at the bottom
st.markdown("<div class='question-input'><div>", unsafe_allow_html=True)
user_input = st.text_input("", placeholder="Ask anything...", key="user_input")
send_button = st.button("Send", key="send_button")

if send_button:
    if user_input:
        st.session_state["last_question"] = user_input
        st.session_state["last_answer"] = ""
        with st.spinner("Generating answer..."):
            answer = chatbot.chat(f"{pdf_content}\n\nQuestion: {user_input}")
            st.session_state["last_answer"] = answer.wait_until_done()
        st.experimental_rerun()
    else:
        st.warning("Please enter a question.")
st.markdown("</div></div>", unsafe_allow_html=True)
