import streamlit as st
from model.speech_analyzer import (
    transcribe_speech_from_mic,
    transcribe_audio_file,
    detect_violence_or_harsh_language
)
import io

# Streamlit UI setup
st.set_page_config(page_title="Speech Analyzer", page_icon="🎤")
st.title("🔊 Voice Harshness & Violence Detector")
st.write("Record your voice or upload an audio file to detect offensive or violent language.")

tab1, tab2 = st.tabs(["🎤 Record Voice", "📁 Upload Audio File"])

# Microphone Recording Tab
with tab1:
    if st.button("Start Recording"):
        try:
            st.info("Listening for your speech...")
            with st.spinner("Processing..."):
                text = transcribe_speech_from_mic()
                st.success("Transcribed Text:")
                st.write(text)

                # Detect violence or harsh language
                result = detect_violence_or_harsh_language(text)
                if "⚠️" in result:
                    st.warning(result)
                else:
                    st.success(result)

        except Exception as e:
            st.error(f"Unexpected error: {e}")

# File Upload Tab
with tab2:
    uploaded_file = st.file_uploader("Upload an audio file (.wav or .mp3)", type=["wav", "mp3"])
    if uploaded_file and st.button("Analyze Uploaded Audio"):
        try:
            st.info("Processing file...")
            with st.spinner("Transcribing audio..."):
                # Load the audio file into memory
                audio_bytes = uploaded_file.read()
                audio_io = io.BytesIO(audio_bytes)

                # Transcribe the audio file to text
                text = transcribe_audio_file(audio_io)
                st.success("Transcribed Text:")
                st.write(text)

                # Analyze the text for violence or harsh language
                result = detect_violence_or_harsh_language(text)
                if "⚠️" in result:
                    st.warning(result)
                else:
                    st.success(result)

                # Play the uploaded audio file from memory without saving to disk
                st.audio(audio_bytes, format="audio/wav")  # Play the uploaded file

        except Exception as e:
            st.error(f"Unexpected error: {e}")
