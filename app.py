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
st.set_page_config(page_title="JayGPT", page_icon=":robot_face:", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .h1 {
        color: black;
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
        caret-color: black;
    }
    .stTextInput>div>div>input:focus {
        border: 2px solid #1a73e8;
        box-shadow: 0 0 10px rgba(26, 115, 232, 0.5);
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
    .response-container {
        margin-top: 20px;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .question-input {
        position: fixed;
        bottom: 0;
        width: 100%;
        padding: 10px;
        background-color: #f0f2f6;
        border-top: 1px solid #ddd;
    }
    .spinner-text {
        color: black !important;
        font-size: 1em;
        font-weight: bold;
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

    .card {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        cursor: pointer;
        text-align: left;
        flex: 1 1 30%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        transition: box-shadow 0.2s ease;
        min-width: 250px;
    }
    .card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border: none;
    }
    .card h3 {
        margin: 0;
        color: black;
    }
    .card p {
        color: grey;
        margin-top: 5px;
        margin-bottom: 0;
    }

    @media (max-width: 768px) {
        .card {
            flex: 1 1 100%;
        }
    }
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

# Pre-defined buttons for quick questions styled as cards
quick_questions = [
    {"title": "Where did Jay complete his education?", "description": "Education background of Jay"},
    {"title": "What professional certifications does Jay hold?", "description": "Certifications Jay has earned"},
    {"title": "What programming languages does Jay know?", "description": "Programming skills of Jay"},
    {"title": "What research has Jay published?", "description": "Research publications by Jay"}
]

# Initialize session state for user input
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

if "generate_answer" not in st.session_state:
    st.session_state["generate_answer"] = False

# Card container using Streamlit columns
columns = st.columns(len(quick_questions))
for i, q in enumerate(quick_questions):
    with columns[i]:
        if st.button(f"{q['title']}"):
            st.session_state["user_input"] = q['title']
            st.session_state["generate_answer"] = True

# Function to create word-by-word typing effect
def typing_effect(text):
    result = ""
    response_container = st.empty()
    words = text.split()
    for word in words:
        result += word + " "
        response_container.markdown(f"<div class='response-container'><div class='bot-response'>{result}</div></div>", unsafe_allow_html=True)
        time.sleep(0.1)  # Adjust the delay as needed


# Fixed input box at the bottom
st.markdown("<div class='question-input'><div>", unsafe_allow_html=True)
user_input = st.text_input("", placeholder="Ask anything...", key="user_input")
send_button = st.button("Send", key="send_button")

# Handle sending the user input or generating the answer from the card click
if send_button or st.session_state["generate_answer"]:
    if st.session_state["user_input"]:
        st.session_state["last_question"] = st.session_state["user_input"]
        st.session_state["last_answer"] = ""
        with st.spinner("Generating answer..."):
            answer = chatbot.chat(f"{pdf_content}\n\nQuestion: {st.session_state['user_input']}")
            st.session_state["last_answer"] = answer.wait_until_done()
        st.session_state["generate_answer"] = False
        st.rerun()
    else:
        st.warning("Please enter a question.")
st.markdown("</div></div>", unsafe_allow_html=True)

# Display the current question and answer
if "last_question" in st.session_state and "last_answer" in st.session_state:
    st.markdown(f"<div class='message'><b class='user-query'>Question:</b> {st.session_state['last_question']}</div>", unsafe_allow_html=True)
    typing_effect(st.session_state['last_answer'])


# remove ui bar top and down
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }

    </style>
    """, unsafe_allow_html=True
)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Hide the header */
    .css-18e3th9 {
        display: none;
    header {visibility: hidden;}

    }
    /* Hide the footer */
    .css-1outpf7 {
        display: none;
    }
    .st-emotion-cache-h4xjwg{
            display: none;
            visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)
