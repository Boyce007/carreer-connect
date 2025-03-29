import streamlit as st
import requests
import fitz  


from streamlit_option_menu import option_menu

from Backend import search_jobs_adzuna
from Backend import search_jobs_linkedin
main_nav = option_menu("Career Connect", ["Job Search", 'Profile', 'Resume Review'], orientation = "horizontal", icons=['house', 'gear'], menu_icon="cast", default_index=1)
SKILL_KEYWORDS = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "AWS", "Azure",
    "Django", "Flask", "React", "Node.js", "Machine Learning", "Deep Learning",
    "Data Science", "Agile", "DevOps", "Git", "Docker", "Kubernetes","Data Structures"
]
def extract_skills(resume_text):
    skills = []
    for skill in SKILL_KEYWORDS:
        if skill.lower() in resume_text.lower():
            skills.append(skill)
    return skills

if main_nav == "Job Search":
    st.title("Job Search")
    job_query = st.text_input("Enter your job search query here:")
    jobs = search_jobs_adzuna('07008', 10, job_query)
    if st.button("Search"):
        if jobs:
            for job in jobs:
                st.subheader(job.get("title", "No Title"))
                company_name = job.get("company", {}).get("display_name", "N/A")
                st.write(f"**Company:** {company_name}")
                location = job.get('location',{}).get("area","N/A")
                st.write(f"**Location:** {location}")
                st.write(f"**Description:** {job.get('description', '')[:200]}...")
                st.markdown(f"[Apply Here]({job.get('redirect_url', '#')})")

        else:
            st.write("No jobs found.")

elif main_nav == "Resume Review":
    st.title("Resume Review")
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
        skills = extract_skills(text)
        for skill in skills:
            jobs = search_jobs_adzuna('07008', 10,skill)
            if jobs:
                for job in jobs:
                    st.subheader(job.get("title", "No Title"))
                    company_name = job.get("company", {}).get("display_name", "N/A")
                    st.write(f"**Company:** {company_name}")
                    location = job.get('location',{}).get("area","N/A")
                    st.write(f"**Location:** {location}")
                    st.write(f"**Description:** {job.get('description', '')[:200]}...")
                    st.markdown(f"[Apply Here]({job.get('redirect_url', '#')})")

            else:
                st.write("No jobs found.")
            
            


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

elif main_nav == "Profile":
    st.title("Profile")

    col1,col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1633332755192-727a05c4013d?q=80&w=2960&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
        new_profile_pic = st.button("Change Profile Picture")
    with col2:
        name = st.text_input("Name")
        bio = st.text_area("Bio")
        skills = st.text_area("Skills")
        location = st.text_input("Location")
        
