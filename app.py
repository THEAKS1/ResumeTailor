import streamlit as st
import io
import pypdf
import docx
import asyncio
import logging
from main_run_file import agent_call_start

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --- Custom CSS for chat bubbles ---
st.markdown("""
<style>
    .chat-user {
        background-color: #DCF8C6; padding:10px; border-radius:12px; 
        margin:5px 0; max-width:80%; margin-left:auto; text-align:right;
    }
    .chat-assistant {
        background-color: #F1F0F0; padding:10px; border-radius:12px; 
        margin:5px 0; max-width:80%; margin-right:auto; text-align:left;
    }
    .stSidebar .stButton button {
        background-color: #4CAF50; color:white; border-radius:8px;
        font-weight:bold; width:100%;
    }
    .stButton button:hover { background-color:#45a049; }
</style>
""", unsafe_allow_html=True)

# --- Helper Function to Process Uploaded Files ---
def get_file_content(uploaded_file):
    try:
        mime_type = uploaded_file.type
        if mime_type == "application/pdf":
            pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            return "\n".join(page.extract_text() for page in pdf_reader.pages)
        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(uploaded_file.getvalue()))
            return "\n".join(para.text for para in doc.paragraphs)
        elif mime_type == "text/plain":
            return uploaded_file.getvalue().decode("utf-8")
        else:
            st.error(f"Unsupported file type: {mime_type}")
            return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# --- Agent Wrapper ---
async def run_resume_agent(resume_text, jd_text, user_name, user_email):
    final_response = await agent_call_start(resume_text, jd_text, user_email)
    yield final_response

# --- Page Config ---
st.set_page_config(page_title="AI Resume Tailor", page_icon="🤖", layout="wide")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.messages = []

# ===================================================================
# 1. LOGIN SCREEN
# ===================================================================
if not st.session_state.logged_in:
    st.title("🤖 AI Resume Tailor")
    st.caption("Smart tailoring of your resume for any job description.")

    with st.form("login_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email Address")
        submitted = st.form_submit_button("Login 🚀")

        if submitted:
            if name and "@" in email:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Please enter a valid name and email.")

# ===================================================================
# 2. MAIN CHAT + SIDEBAR INPUT
# ===================================================================
else:
    st.subheader(f"Welcome back, {st.session_state.user_name}! 👋")

    # --- Sidebar ---
    st.sidebar.header("📂 Provide Your Documents")
    input_method = st.sidebar.radio("Input method:", ("Upload Files", "Paste Text"))

    resume_content, jd_content = None, None
    if input_method == "Upload Files":
        resume_file = st.sidebar.file_uploader("Upload Resume", type=['pdf','docx','txt'])
        jd_file = st.sidebar.file_uploader("Upload Job Description", type=['pdf','docx','txt'])
        if resume_file:
            resume_content = get_file_content(resume_file)
            st.sidebar.success(f"✅ Resume uploaded: {resume_file.name}")
        if jd_file:
            jd_content = get_file_content(jd_file)
            st.sidebar.success(f"✅ JD uploaded: {jd_file.name}")
    else:
        resume_text = st.sidebar.text_area("Paste Resume", height=150)
        jd_text = st.sidebar.text_area("Paste Job Description", height=150)
        if resume_text: resume_content = resume_text
        if jd_text: jd_content = jd_text

    # --- Chat Messages ---
    st.markdown("### 💬 Conversation")
    if not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hi there! Upload your resume and job description, then hit **✨ Tailor My Resume** in the sidebar."
        })

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='chat-user'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-assistant'>{message['content']}</div>", unsafe_allow_html=True)

    # --- Tailor Resume Button ---
    if st.sidebar.button("✨ Tailor My Resume"):
        if resume_content and jd_content:
            st.session_state.messages.append({"role": "user", "content": "Here are my resume and JD. Tailor it."})
            st.markdown(f"<div class='chat-user'>Here are my resume and JD. Tailor it.</div>", unsafe_allow_html=True)

            with st.spinner("🤖 Your career assistant is tailoring..."):
                async def get_agent_response():
                    full_response = ""
                    async for chunk in run_resume_agent(
                        resume_content, jd_content,
                        st.session_state.user_name, st.session_state.user_email
                    ):
                        full_response += chunk
                    return full_response

                try:
                    full_response = asyncio.run(get_agent_response())
                except Exception as e:
                    full_response = f"⚠️ Error: {e}"

            st.markdown(f"<div class='chat-assistant'>{full_response}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.sidebar.warning("⚠️ Please provide both your resume and job description.")

    # --- Clear Chat ---
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
