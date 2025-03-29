import fitz
import streamlit as st
import requests

st.title("📄 PDF Resume Reader +  Job Suggestion")

uploaded_pdf = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": "Bearer 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"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if uploaded_pdf:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    doc = fitz.open("temp_resume.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    st.subheader("📝 Extracted Resume Text:")
    st.write(text)

    if st.button("🔍 Analyze Resume with AI"):
        st.info("Thinking... 🔄")
        prompt = f"""
        You are an expert career advisor AI.

        Read the following resume carefully. Based on the skills, work experience, education, and technologies mentioned, suggest the most suitable job title that matches this person’s profile.

        Be specific and thoughtful. Only return the best matching job title, like "Backend Developer", "IT Support Specialist", or "Data Analyst".

        Do not explain — just return the job title.

        Resume:
        {text}
        """

        result = query({"inputs": prompt})

        if isinstance(result, list):
            job_suggestion = result[0]["generated_text"]
        elif "generated_text" in result:
            job_suggestion = result["generated_text"]
        else:
            job_suggestion = "No valid suggestion received."

        st.session_state["job_suggestion"] = job_suggestion

        st.subheader("💼 Job Suggestion:")
        st.write(job_suggestion)

if st.button(" Apply Now"):
    job_query = st.session_state['job_suggestion'].strip().replace(" ", "+")
    job_url = f"https://www.google.com/search?q={job_query}+jobs+near+me"

    st.success(" here are the job openings for:")
    st.markdown(f"### 🔗 [Click here to view '{st.session_state['job_suggestion']}' jobs near you]({job_url})")


