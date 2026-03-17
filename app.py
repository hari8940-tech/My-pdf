st.html(<meta name="google-site-verification" content="hqxCx4AQdaHL1M9LpRWj7XSrsVOErPlI0HrKHPe_8C0" />)
st.set_page_config(
    page_title="EditMyPDF | Free AI PDF & Word Editor",
    page_icon="🖋️",
    menu_items={
        'About': "# EditMyPDF\nThe best free AI tool to summarize and edit documents."
    }
)

import streamlit as st
import google.generativeai as genai

# This line looks for the secret you just saved in Step 1
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Please add your GEMINI_API_KEY to the Streamlit Secrets!")

import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from fpdf import FPDF
import google.generativeai as genai

# Securely load your key from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")

def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

st.set_page_config(page_title="AI Editor", page_icon="🖋️")
st.title("🖋️ Simple AI Document Editor")

uploaded_file = st.file_uploader("Upload PDF or Word", type=["pdf", "docx"])

if uploaded_file:
    text = extract_text(uploaded_file)
    task = st.text_input("What should AI do?", "Summarize this document clearly.")
    
    if st.button("Process"):
        with st.spinner("AI is editing..."):
            response = model.generate_content(f"{task}\n\n{text}")
            st.session_state['out'] = response.text
            st.success("Success!")

    if 'out' in st.session_state:
        st.text_area("Result", st.session_state['out'], height=300)
        st.download_button("Download Result (Text)", st.session_state['out'], "edited.txt")
