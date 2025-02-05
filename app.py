import streamlit as st
import whisper
import tempfile
import os
from streamlit_audio_recorder import audio_recorder  # For real-time audio recording

# Load the Whisper model once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")  # Options: "tiny", "base", "small", "medium", "large"

model = load_whisper_model()

st.title("Whisper AI Local Transcription")

# Let user choose between uploading a file or recording audio in real time
input_method = st.radio("Select Input Method", ("Upload Audio File", "Record Audio"))

audio_data = None

if input_method == "Upload Audio File":
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "m4a"])
    if uploaded_file is not None:
        audio_data = uploaded_file.read()
        # Display audio player (format is derived from the file type)
        st.audio(audio_data, format=f"audio/{uploaded_file.type.split('/')[-1]}")
elif input_method == "Record Audio":
    st.write("Record your audio:")
    # The recorder returns audio bytes (typically in WAV format)
    audio_bytes = audio_recorder()
    if audio_bytes is not None:
        audio_data = audio_bytes
        st.audio(audio_bytes, format="audio/wav")

if audio_data is not None:
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            # Save the audio data to a temporary file (using .wav extension for simplicity)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio_path = temp_audio.name
                temp_audio.write(audio_data)

            try:
                # Load and process the audio using Whisper
                audio = whisper.load_audio(temp_audio_path)
                audio = whisper.pad_or_trim(audio)
                mel = whisper.log_mel_spectrogram(audio).to(model.device)

                # Detect language
                _, probs = model.detect_language(mel)
                detected_lang = max(probs, key=probs.get)

                # Transcribe the audio
                result = model.transcribe(temp_audio_path)
                transcription_text = result["text"]

                st.success(f"Detected Language: {detected_lang.upper()}")
                st.text_area("Transcription", transcription_text, height=200)

                # Create a temporary text file to save the transcription
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_txt:
                    temp_txt_path = temp_txt.name
                    temp_txt.write(transcription_text.encode("utf-8"))
                    temp_txt.flush()

                # Provide a download button for the TXT file
                with open(temp_txt_path, "rb") as f:
                    st.download_button(
                        label="Download Transcription",
                        data=f,
                        file_name="transcription.txt",
                        mime="text/plain"
                    )
            finally:
                # Clean up temporary files
                os.remove(temp_audio_path)
                if 'temp_txt_path' in locals():
                    os.remove(temp_txt_path)
