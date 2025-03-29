import fitz  # PyMuPDF
import streamlit as st

st.title("📄 PDF Resume Reader")

uploaded_pdf = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_pdf:
    try:
        # Open the PDF directly from the uploaded file
        doc = fitz.open(stream=uploaded_pdf.getbuffer(), filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text() + "\n"

        if text.strip():
            st.subheader("📝 Extracted Resume Text:")
            st.write(text)
        else:
            st.warning("No text could be extracted. This PDF may be image-based.")

    except Exception as e:
        st.error(f"An error occurred while reading the PDF: {e}")