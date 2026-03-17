import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from fpdf import FPDF
import google.generativeai as genai

# 1. GOOGLE SEARCH VERIFICATION (Add this for Google to find you)
st.html('<meta name="google-site-verification" content="google957e0fe0b2f33b18" />')

# 2. APP CONFIGURATION & SEO
st.set_page_config(
    page_title="EditMyPDF - AI Powered Document Editor",
    page_icon="🖋️",
    layout="wide"
)

# 3. SECURE AI CONNECTION
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ AI Key Missing! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")

# 4. DOCUMENT PROCESSING FUNCTIONS
def extract_text(file):
    """Extracts text from PDF or Word files."""
    try:
        if file.type == "application/pdf":
            doc = fitz.open(stream=file.read(), filetype="pdf")
            return "".join([page.get_text() for page in doc])
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return ""

def create_pdf(text):
    """Turns AI result into a downloadable PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Encodes text to avoid errors with special characters
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')

# 5. USER INTERFACE (UI)
st.title("🖋️ EditMyPDF: AI Document Assistant")
st.markdown("---")

# Sidebar for Instructions
with st.sidebar:
    st.header("How to use")
    st.write("1. Upload a PDF or Word file.")
    st.write("2. Tell the AI what to do (Summarize, Translate, etc).")
    st.write("3. Download your edited version as a new PDF.")
    st.divider()
    st.info("Your files are processed securely and not stored permanently.")

# Main Upload Section
uploaded_file = st.file_uploader("Upload your document (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    original_text = extract_text(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Content")
        st.text_area("Original Text View", original_text, height=450)

    with col2:
        st.subheader("AI Editor")
        instruction = st.text_input("What should the AI do?", placeholder="e.g. 'Summarize this in 5 bullet points'")
        
        if st.button("✨ Process Document"):
            if instruction:
                with st.spinner("AI is working its magic..."):
                    prompt = f"Act as a professional document editor. {instruction}:\n\n{original_text}"
                    response = model.generate_content(prompt)
                    st.session_state['ai_result'] = response.text
                    st.success("Done!")
            else:
                st.warning("Please enter an instruction first.")

        # Results and Downloads
        if 'ai_result' in st.session_state:
            st.text_area("AI Result", st.session_state['ai_result'], height=300)
            
            # Export Buttons
            pdf_bytes = create_pdf(st.session_state['ai_result'])
            
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_bytes,
                file_name="AI_Edited_Document.pdf",
                mime="application/pdf"
            )
            
            st.download_button(
                label="📄 Download as Text",
                data=st.session_state['ai_result'],
                file_name="AI_Edited_Document.txt"
            )
