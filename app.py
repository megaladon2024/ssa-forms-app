import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import io

recognizer = sr.Recognizer()

st.title("SSA Forms Assistant (SSA-3369-BK & SSA-3373-BK)")
st.write("Use your voice or type your answers to populate your forms.")

def record_voice_robust():
    """Alternative recorder using sounddevice (Works out of the box on Windows)"""
    status_box = st.empty()
    status_box.info("🎙️ Initializing recorder...")
    
    fs = 16000  # Standard recording rate
    duration = 6  # Recording length in seconds
    
    status_box.success(f"🔴 Recording for {duration} seconds... Speak Now!")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording window to finish
    
    status_box.text("🤖 Processing speech data...")
    
    wav_io = io.BytesIO()
    wav.write(wav_io, fs, audio_data)
    wav_io.seek(0)
    
    with sr.AudioFile(wav_io) as source:
        audio = recognizer.record(source)
        try:
            transcribed_text = recognizer.recognize_google(audio)
            status_box.empty()
            return transcribed_text
        except Exception:
            status_box.warning("🤷 Could not interpret the audio recording. Please type below.")
            return ""

# Simple test input field to verify app works
user_input = st.text_input("Type your answer or click below to speak:")
if st.button("🎤 Speak Answer"):
    spoken = record_voice_robust()
    if spoken:
        st.write(f"You said: {spoken}")