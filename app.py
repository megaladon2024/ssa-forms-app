import streamlit as st
import speech_recognition as sr
import io
from pypdf import PdfReader, PdfWriter

# Page Configuration
st.set_page_config(page_title="SSA Forms Assistant", page_icon="📝", layout="wide")

recognizer = sr.Recognizer()

st.title("📝 SSA Forms Assistant")
st.write("Complete SSA-3369-BK (Work History) & SSA-3373-BK (Function Report) using voice or text for each question.")

# --- Helper Function for Voice Recognition ---
def process_audio(audio_file):
    """Processes audio recording from st.audio_input using Google Speech Recognition."""
    if audio_file is not None:
        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                return recognizer.recognize_google(audio)
        except Exception:
            st.warning("Could not clearly interpret the recording. Please type your answer or try recording again.")
            return ""
    return ""

# Sidebar Navigation
form_selection = st.sidebar.radio("Select Form to Fill:", ["SSA-3369-BK (Work History)", "SSA-3373-BK (Function Report)"])

# --- PDF GENERATION UTILITY ---
def populate_pdf(template_path, field_dictionary):
    """Reads a PDF template, fills fillable fields, and returns a downloadable BytesIO buffer."""
    reader = PdfReader(template_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.update_page_form_field_values(writer.pages[0], field_dictionary)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream


# --- FORM 1: SSA-3369-BK (Work History Report) ---
if form_selection == "SSA-3369-BK (Work History)":
    st.header("SSA-3369-BK: Work History Report")
    
    st.subheader("Section 1 - Information About You")
    
    st.markdown("**1.A Claimant's Full Name**")
    audio_name = st.audio_input("Record Name", key="aud_3369_name")
    val_name = process_audio(audio_name) if audio_name else ""
    claimant_name = st.text_input("Full Name:", value=val_name, key="txt_3369_name")

    st.markdown("**1.B Social Security Number**")
    audio_ssn = st.audio_input("Record SSN", key="aud_3369_ssn")
    val_ssn = process_audio(audio_ssn) if audio_ssn else ""
    ssn_number = st.text_input("Social Security Number:", value=val_ssn, key="txt_3369_ssn")

    st.markdown("**1.C Daytime Phone Number**")
    audio_phone = st.audio_input("Record Phone Number", key="aud_3369_phone")
    val_phone = process_audio(audio_phone) if audio_phone else ""
    phone_number = st.text_input("Daytime Phone Number:", value=val_phone, key="txt_3369_phone")

    st.subheader("Section 2 - Work History (Job No. 1)")
    
    st.markdown("**Job Title #1**")
    audio_job = st.audio_input("Record Job Title", key="aud_3369_job")
    val_job = process_audio(audio_job) if audio_job else ""
    job_title_1 = st.text_input("Job Title:", value=val_job, key="txt_3369_job")

    st.markdown("**Type of Business**")
    audio_biz = st.audio_input("Record Business Type", key="aud_3369_biz")
    val_biz = process_audio(audio_biz) if audio_biz else ""
    business_type = st.text_input("Business Type:", value=val_biz, key="txt_3369_biz")

    st.markdown("**Dates Worked**")
    audio_dates = st.audio_input("Record Dates Worked", key="aud_3369_dates")
    val_dates = process_audio(audio_dates) if audio_dates else ""
    dates_worked = st.text_input("Dates Worked (e.g., 01/2018 to 05/2022):", value=val_dates, key="txt_3369_dates")

    st.markdown("**Rate of Pay**")
    audio_pay = st.audio_input("Record Rate of Pay", key="aud_3369_pay")
    val_pay = process_audio(audio_pay) if audio_pay else ""
    rate_of_pay = st.text_input("Rate of Pay:", value=val_pay, key="txt_3369_pay")

    st.markdown("**Daily Tasks and Duties**")
    audio_duties = st.audio_input("Record Job Duties", key="aud_3369_duties")
    val_duties = process_audio(audio_duties) if audio_duties else ""
    job_duties = st.text_area("Describe your tasks and duties:", value=val_duties, key="txt_3369_duties")

    st.markdown("**Machines, Tools, or Equipment Used**")
    audio_tools = st.audio_input("Record Machines/Tools", key="aud_3369_tools")
    val_tools = process_audio(audio_tools) if audio_tools else ""
    machines_tools = st.text_area("List equipment used:", value=val_tools, key="txt_3369_tools")

    st.subheader("Physical Requirements")
    col1, col2 = st.columns(2)
    with col1:
        walk_hours = st.selectbox("Hours spent standing/walking:", range(0, 13))
        sit_hours = st.selectbox("Hours spent sitting:", range(0, 13))
        climb_hours = st.selectbox("Hours spent climbing:", range(0, 13))
    with col2:
        stoop_hours = st.selectbox("Hours spent stooping/bending:", range(0, 13))
        kneel_hours = st.selectbox("Hours spent kneeling:", range(0, 13))
        heaviest_weight = st.selectbox("Heaviest weight lifted:", ["Less than 10 lbs", "10 lbs", "20 lbs", "50 lbs", "100+ lbs"])

    st.subheader("Section 3 - Remarks")
    st.markdown("**Additional Remarks**")
    audio_remarks = st.audio_input("Record Remarks", key="aud_3369_remarks")
    val_remarks = process_audio(audio_remarks) if audio_remarks else ""
    remarks = st.text_area("Additional remarks:", value=val_remarks, key="txt_3369_remarks")

    st.write("---")
    if st.button("Generate SSA-3369-BK PDF", type="primary"):
        form_fields = {
            "NAME": claimant_name,
            "SSN": ssn_number,
            "PHONE": phone_number,
            "JOB_TITLE_1": job_title_1,
            "BUSINESS": business_type,
            "DATES": dates_worked,
            "PAY": rate_of_pay,
            "DUTIES": job_duties,
            "TOOLS": machines_tools,
            "REMARKS": remarks
        }
        try:
            pdf_buffer = populate_pdf("ssa_3369.pdf", form_fields)
            st.success("SSA-3369-BK generated successfully!")
            st.download_button(
                label="📥 Download Filled SSA-3369-BK PDF",
                data=pdf_buffer,
                file_name="Completed_SSA-3369-BK.pdf",
                mime="application/pdf"
            )
        except Exception:
            st.warning("Generated form data summary (Add 'ssa_3369.pdf' to repository root for direct PDF download):")
            st.json(form_fields)


# --- FORM 2: SSA-3373-BK (Function Report - Adult) ---
elif form_selection == "SSA-3373-BK (Function Report)":
    st.header("SSA-3373-BK: Function Report - Adult")
    
    st.subheader("Section A - General Information")
    
    st.markdown("**1. Full Legal Name**")
    audio_3373_name = st.audio_input("Record Name", key="aud_3373_name")
    val_3373_name = process_audio(audio_3373_name) if audio_3373_name else ""
    claimant_name = st.text_input("Full Name:", value=val_3373_name, key="txt_3373_name")

    st.markdown("**2. Social Security Number**")
    audio_3373_ssn = st.audio_input("Record SSN", key="aud_3373_ssn")
    val_3373_ssn = process_audio(audio_3373_ssn) if audio_3373_ssn else ""
    ssn_number = st.text_input("Social Security Number:", value=val_3373_ssn, key="txt_3373_ssn")

    st.markdown("**3. Daytime Telephone Number**")
    audio_3373_phone = st.audio_input("Record Phone", key="aud_3373_phone")
    val_3373_phone = process_audio(audio_3373_phone) if audio_3373_phone else ""
    phone_number = st.text_input("Telephone Number:", value=val_3373_phone, key="txt_3373_phone")

    st.subheader("Section B - Information About Illnesses / Conditions")
    st.markdown("**5. How do your conditions limit your ability to work?**")
    audio_impact = st.audio_input("Record Work Limitations", key="aud_3373_impact")
    val_impact = process_audio(audio_impact) if audio_impact else ""
    illness_impact = st.text_area("Describe limitations:", value=val_impact, key="txt_3373_impact")

    st.subheader("Section C - Daily Activities")
    
    st.markdown("**6. Daily Routine (Wake up to bedtime)**")
    audio_routine = st.audio_input("Record Daily Routine", key="aud_3373_routine")
    val_routine = process_audio(audio_routine) if audio_routine else ""
    daily_routine = st.text_area("Describe daily activities:", value=val_routine, key="txt_3373_routine")

    st.markdown("**8. Care of Pets or Animals**")
    audio_pets = st.audio_input("Record Pet Care Details", key="aud_3373_pets")
    val_pets = process_audio(audio_pets) if audio_pets else ""
    pet_care = st.text_area("Describe care for animals:", value=val_pets, key="txt_3373_pets")

    st.markdown("**11. Effect on Sleep**")
    audio_sleep = st.audio_input("Record Sleep Effects", key="aud_3373_sleep")
    val_sleep = process_audio(audio_sleep) if audio_sleep else ""
    sleep_impact = st.text_area("Describe sleep issues:", value=val_sleep, key="txt_3373_sleep")

    st.markdown("**12. Personal Care (Dressing, Bathing, Feeding, etc.)**")
    audio_care = st.audio_input("Record Personal Care Details", key="aud_3373_care")
    val_care = process_audio(audio_care) if audio_care else ""
    personal_care = st.text_area("Describe personal care challenges:", value=val_care, key="txt_3373_care")

    st.markdown("**13. Meal Preparation**")
    audio_meals = st.audio_input("Record Meal Prep Details", key="aud_3373_meals")
    val_meals = process_audio(audio_meals) if audio_meals else ""
    cooking_habits = st.text_area("Describe meal preparation:", value=val_meals, key="txt_3373_meals")

    st.markdown("**14. House and Yard Work**")
    audio_chores = st.audio_input("Record House/Yard Work", key="aud_3373_chores")
    val_chores = process_audio(audio_chores) if audio_chores else ""
    house_yard_work = st.text_area("Describe household chores:", value=val_chores, key="txt_3373_chores")

    st.subheader("Section D - Information About Abilities")
    
    st.markdown("**Walking Limitations**")
    audio_walk = st.audio_input("Record Walking Limits", key="aud_3373_walk")
    val_walk = process_audio(audio_walk) if audio_walk else ""
    walking_limit = st.text_input("How far can you walk before needing rest?", value=val_walk, key="txt_3373_walk")

    st.markdown("**Instructions**")
    audio_instruct = st.audio_input("Record Instruction Details", key="aud_3373_instruct")
    val_instruct = process_audio(audio_instruct) if audio_instruct else ""
    following_instructions = st.text_area("How well do you follow written and spoken instructions?", value=val_instruct, key="txt_3373_instruct")

    st.subheader("Section E - Remarks")
    st.markdown("**Additional Remarks**")
    audio_remarks_3373 = st.audio_input("Record Remarks", key="aud_3373_remarks")
    val_remarks_3373 = process_audio(audio_remarks_3373) if audio_remarks_3373 else ""
    remarks_3373 = st.text_area("Additional remarks:", value=val_remarks_3373, key="txt_3373_remarks")

    st.write("---")
    if st.button("Generate SSA-3373-BK PDF", type="primary"):
        form_fields_3373 = {
            "NAME": claimant_name,
            "SSN": ssn_number,
            "PHONE": phone_number,
            "LIMITATIONS": illness_impact,
            "DAILY_ROUTINE": daily_routine,
            "PETS": pet_care,
            "SLEEP": sleep_impact,
            "PERSONAL_CARE": personal_care,
            "MEALS": cooking_habits,
            "CHORES": house_yard_work,
            "WALKING": walking_limit,
            "INSTRUCTIONS": following_instructions,
            "REMARKS": remarks_3373
        }
        try:
            pdf_buffer = populate_pdf("ssa_3373.pdf", form_fields_3373)
            st.success("SSA-3373-BK generated successfully!")
            st.download_button(
                label="📥 Download Filled SSA-3373-BK PDF",
                data=pdf_buffer,
                file_name="Completed_SSA-3373-BK.pdf",
                mime="application/pdf"
            )
        except Exception:
            st.warning("Generated form data summary (Add 'ssa_3373.pdf' to repository root for direct PDF download):")
            st.json(form_fields_3373)
