import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Master Pro", page_icon="📄")

st.title("📄 PDF Master Pro")
st.sidebar.header("Navigation")
action = st.sidebar.selectbox("Choose Tool", ["Merge PDFs", "Split PDF", "Protect PDF"])

if action == "Merge PDFs":
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if files and st.button("Merge"):
        writer = PdfWriter()
        for f in files: writer.append(f)
        out = io.BytesIO()
        writer.write(out)
        st.download_button("Download Merged PDF", out.getvalue(), "merged.pdf")

elif action == "Split PDF":
    file = st.file_uploader("Upload PDF", type="pdf")
    if file:
        reader = PdfReader(file)
        pg = st.number_input("Page to extract", min_value=1, max_value=len(reader.pages))
        if st.button("Extract"):
            writer = PdfWriter()
            writer.add_page(reader.pages[pg-1])
            out = io.BytesIO()
            writer.write(out)
            st.download_button("Download Page", out.getvalue(), "split.pdf")

elif action == "Protect PDF":
    file = st.file_uploader("Upload PDF", type="pdf")
    pwd = st.text_input("Set Password", type="password")
    if file and pwd and st.button("Encrypt"):
        reader = PdfReader(file)
        writer = PdfWriter()
        for p in reader.pages: writer.add_page(p)
        writer.encrypt(pwd)
        out = io.BytesIO()
        writer.write(out)
        st.download_button("Download Protected PDF", out.getvalue(), "protected.pdf")