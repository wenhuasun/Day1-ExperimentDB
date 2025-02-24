import sys
if sys.version_info.major < 3 or sys.version_info.minor != 10:
    raise RuntimeError("This script should be run by exactly Python 3.10.")


import streamlit as st
from tinydb import TinyDB, Query
from datetime import date

# Initialize TinyDB with two tables: one for subjects and one for sessions.
db = TinyDB("db.json")
subjects_table = db.table("subjects")
sessions_table = db.table("sessions")

# Page Title and Experiment Description
st.title("Visual Perception Experiment for Rats")
st.subheader("MPI Florida")
st.write("""
Welcome to the experiment logging application for our Visual Perception Experiment conducted at MPI Florida. 
In this study, we investigate how rats respond to various visual stimuli under different experimental conditions. 
Use the sidebar to navigate and log new subjects or sessions, and to view the recorded data.
""")

# Sidebar navigation
st.sidebar.title("Navigation")
action = st.sidebar.radio("Select Action", 
                          ["Add Subject", "Add Session", "View Subjects", "View Sessions"])

if action == "Add Subject":
    st.header("Add New Subject")
    st.write("Please enter the details for the rat subject participating in the experiment.")
    with st.form("subject_form", clear_on_submit=True):
        subject_id = st.text_input("Subject ID")
        name = st.text_input("Name")
        dob = st.date_input("Date of Birth", value=date(2020, 1, 1))
        sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
        submitted = st.form_submit_button("Add Subject")
        if submitted:
            if subject_id and name:
                subjects_table.insert({
                    "id": subject_id,
                    "name": name,
                    "dob": dob.isoformat(),
                    "sex": sex
                })
                st.success(f"Subject {name} added successfully!")
            else:
                st.error("Subject ID and Name are required fields.")

elif action == "Add Session":
    st.header("Log New Session")
    st.write("Select a subject and enter the session details for the experiment.")
    subjects = subjects_table.all()
    if not subjects:
        st.warning("No subjects available. Please add subjects first.")
    else:
        # Create a dictionary to map display names to subject records
        subject_options = {f"{sub['id']} - {sub['name']}": sub for sub in subjects}
        with st.form("session_form", clear_on_submit=True):
            selected_subject = st.selectbox("Select Subject", options=list(subject_options.keys()))
            session_date = st.date_input("Session Date", value=date.today())
            condition = st.text_input("Experimental Condition", 
                                      placeholder="e.g., High Contrast, Low Light, etc.")
            notes = st.text_area("Notes", 
                                 placeholder="Enter any observations or additional details about the session.")
            submitted = st.form_submit_button("Add Session")
            if submitted:
                session_data = {
                    "subject_id": subject_options[selected_subject]["id"],
                    "session_date": session_date.isoformat(),
                    "condition": condition,
                    "notes": notes
                }
                sessions_table.insert(session_data)
                st.success("Session logged successfully!")

elif action == "View Subjects":
    st.header("Subjects Table")
    st.write("Below is a list of all rat subjects registered for the Visual Perception Experiment.")
    subjects = subjects_table.all()
    if subjects:
        st.table(subjects)
    else:
        st.info("No subjects found. Please add some subjects to begin.")

elif action == "View Sessions":
    st.header("Sessions Table")
    st.write("Below is a record of all experimental sessions logged for the Visual Perception Experiment.")
    sessions = sessions_table.all()
    if sessions:
        st.table(sessions)
    else:
        st.info("No sessions found. Please log some sessions.")