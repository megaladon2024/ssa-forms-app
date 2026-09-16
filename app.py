import streamlit as st
import speech_recognition as sr
import io
from pypdf import PdfReader, PdfWriter

# Page Configuration
st.set_page_config(page_title="SSA Forms Assistant", page_icon="📝", layout="wide")

recognizer = sr.Recognizer()

st.title("📝 SSA Forms Assistant")
st.write("Complete SSA-3369-BK (Work History) & SSA-3373-BK (Function Report) using voice or text.")

# --- Helper Function for Voice Recognition ---
def process_audio(audio_file):
    if audio_file is not None:
        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                return recognizer.recognize_google(audio)
        except Exception:
            st.warning("Could not clearly interpret the audio. Please type or edit below.")
            return ""
    return ""

# Sidebar Navigation
form_selection = st.sidebar.radio("Select Form to Fill:", ["SSA-3369-BK (Work History)", "SSA-3373-BK (Function Report)"])

st.sidebar.divider()
st.sidebar.header("🎙️ Voice Input")
audio_input = st.audio_input("Record an answer:")
transcribed_voice = process_audio(audio_input) if audio_input else ""

if transcribed_voice:
    st.sidebar.success(f"Transcribed: '{transcribed_voice}'")

# --- FORM 1: SSA-3369-BK (Work History Report) ---
if form_selection == "SSA-3369-BK (Work History)":
    st.header("SSA-3369-BK: Work History Report")
    
    with st.form("ssa_3369_form"):
        st.subheader("Section 1 - Information About Your Work")
        
        applicant_name = st.text_input("Claimant's Full Name:", value=transcribed_voice if transcribed_voice else "")
        ssn_last4 = st.text_input("Social Security Number (Last 4 Digits):")
        
        job_title_1 = st.text_input("Job Title #1 (Most Recent):")
        rate_of_pay = st.text_input("Rate of Pay (e.g., $15/hour or $30,000/year):")
        hours_per_week = st.text_input("Average Hours Worked Per Week:")
        
        job_duties = st.text_area("Describe what you did in this job (machinery used, lifting, writing, etc.):")
        
        st.subheader("Physical Requirements of Job #1")
        col1, col2 = st.columns(2)
        with col1:
            walk_hours = st.selectbox("In a normal workday, how many hours did you walk?", range(0, 9))
            stand_hours = st.selectbox("In a normal workday, how many hours did you stand?", range(0, 9))
            sit_hours = st.selectbox("In a normal workday, how many hours did you sit?", range(0, 9))
        with col2:
            climb_hours = st.selectbox("In a normal workday, how many hours did you climb?", range(0, 9))
            stoop_hours = st.selectbox("In a normal workday, how many hours did you stoop/bend?", range(0, 9))
            heaviest_weight = st.selectbox("Heaviest weight lifted:", ["10 lbs or less", "20 lbs", "50 lbs", "100+ lbs"])

        submit_3369 = st.form_submit_button("Generate & Save SSA-3369-BK Data")

    if submit_3369:
        st.success("Work History entries saved successfully. Ready for PDF download/print.")

# --- FORM 2: SSA-3373-BK (Function Report - Adult) ---
elif form_selection == "SSA-3373-BK (Function Report)":
    st.header("SSA-3373-BK: Function Report - Adult")
    
    with st.form("ssa_3373_form"):
        st.subheader("Section A - General Information & Daily Activities")
        
        claimant_name = st.text_input("Full Legal Name:", value=transcribed_voice if transcribed_voice else "")
        illness_impact = st.text_area("How do your illnesses, injuries, or conditions limit your ability to work?")
        
        daily_routine = st.text_area("Describe what you do from the time you wake up until you go to bed:")
        
        st.subheader("Personal Care & Daily Living")
        care_pets = st.text_area("Do you take care of pets or other people? (If yes, describe):")
        sleep_issues = st.text_area("How does your condition affect your sleep?")
        
        st.subheader("Mobility & Physical Abilities")
        lifting_limit = st.text_input("How much weight can you lift/carry?")
        walking_limit = st.text_input("How far can you walk before needing to stop and rest?")
        rest_time = st.text_input("How long do you need to rest before you can start walking again?")
        
        submit_3373 = st.form_submit_button("Generate & Save SSA-3373-BK Data")

    if submit_3373:
        st.success("Function Report entries saved successfully. Ready for PDF download/print.")
