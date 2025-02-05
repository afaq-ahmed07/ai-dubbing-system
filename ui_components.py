import streamlit as st
from audio_recorder_streamlit import audio_recorder

def get_user_input():
    """Handle user input selection (Upload Audio, Record Audio, Upload Video)."""
    input_method = st.radio("Select Input Method", ("Upload Audio File", "Record Audio", "Upload Video File"))

    audio_data = None
    video_data = None

    try:
        if input_method == "Upload Audio File":
            uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "m4a"])
            if uploaded_file is not None:
                audio_data = uploaded_file.read()
                st.audio(audio_data, format="audio/wav")  # Use a safe default format

        elif input_method == "Record Audio":
            st.write("Record your audio:")
            audio_bytes = audio_recorder()
            if audio_bytes:
                audio_data = audio_bytes
                st.audio(audio_bytes, format="audio/wav")

        elif input_method == "Upload Video File":
            uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
            if uploaded_video:
                video_data = uploaded_video.read()

    except Exception as e:
        st.error(f"An error occurred: {e}")  # Display errors instead of crashing

    return audio_data, video_data
