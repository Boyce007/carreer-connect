import streamlit as st
import requests

from streamlit_option_menu import option_menu

from Backend.Backend import search_jobs_adzuna
from Backend.Backend import search_jobs_linkedin

main_nav = option_menu("Career Connect", ["Job Search", 'Job Apply', 'Profile', 'Favorites'], orientation = "horizontal", icons=['house', 'gear'], menu_icon="cast", default_index=1)

if main_nav == "Job Search":
    st.title("Job Search")
    st.text_input("Enter your job search query here:")
    # search_jobs_adzuna(, 10, st.title)
    st.button("Search")


elif main_nav == "Job Apply":
    st.title("Job Apply")
    st.write("This is the Job Apply page.")

elif main_nav == "Favorites":
    st.title("Favorites")
    st.write("This is your favorites jobs saved.")

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
        if st.button("Experience"):
            st.switch_page("pages/experience.py")
