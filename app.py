import streamlit as st
import google.generativeai as genai

# ------------------------------
# Configure Gemini API
# ------------------------------
GEMINI_API_KEY = "AIzaSyC3cFwUBOCQkI-AswaI9XjHhx-zquqPKm4"
genai.configure(api_key=GEMINI_API_KEY)

# ------------------------------
# Streamlit page config & CSS
# ------------------------------
st.set_page_config(page_title="AgroBot 🌾", layout="wide")

# Custom CSS to match your color scheme
st.markdown("""
<style>
body {
    background-color: #E9F3F0;
    font-family: "Segoe UI", Arial, sans-serif;
}
header {
    background-color: #1EAC53;
    color: white;
    padding: 10px 20px;
    font-size: 20px;
    font-weight: 600;
}
.sidebar .sidebar-content {
    background-color: #ffffff;
}
.stButton>button {
    background-color: #FFC107;
    color: white;
    border-radius: 10px;
    border: none;
    height: 38px;
    width: 100% !important;
    text-align: left;
    padding-left: 10px;
    margin-bottom: 5px;
}
.stButton>button:hover {
    background-color: #e0a800;
}
.stTextInput>div>div>input {
    border-radius: 25px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar content with logo
# ------------------------------
with st.sidebar:
    # Logo on top
    st.markdown("# Agro Bot")  # Make sure logo.png is in the same folder
    st.markdown("## About")
    st.markdown(
        "**AgroBot** is your assistant for exploring **crop prices**, **market trends**, "
        "and **farming insights**. Designed to give farmers and analysts quick, clear, "
        "and actionable knowledge."
    )

    st.markdown("## Quick Tips")
    quick_questions = [
        ("🌾 Best time to buy wheat   ", "When should I buy wheat in Pakistan?"),
        ("🏙️ Cheapest city for rice  ", "Which city has the lowest rice price in Pakistan?"),
        ("📊 MoM Inflation explained    ", "Explain MoM inflation"),
        ("📅 Cotton seasonal trends                         ", "What are the seasonal price trends of Cotton in Pakistan?"),
        ("🌾 Top inflation driver    ", "Which crop contributed most to inflation last year in Pakistan?")
    ]
    
    # Buttons with equal width
    for label, question in quick_questions:
        if st.button(label, key=label):
            st.session_state.user_input = question

    st.markdown("---")
    st.markdown("### Credits")
    st.markdown("Built by Muhammad Hassan")

# ------------------------------
# Chat area
# ------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Input box
user_input = st.text_input("Ask me anything...", st.session_state.user_input)
st.session_state.user_input = ""  # reset after taking input

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate bot response
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = "⚠️ Sorry, I couldn’t connect to Gemini."

    st.session_state.chat_history.append({"role": "bot", "content": bot_reply})

# Display chat messages
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    else:
        st.chat_message("assistant").write(chat["content"])
