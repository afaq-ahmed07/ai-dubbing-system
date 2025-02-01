import streamlit as st
import whisper
import tempfile
import os

# Load Whisper model once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")  # Use "small", "medium", or "large" if needed

model = load_whisper_model()

st.title("Whisper AI Local Transcription")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[-1]}")

    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            # Save the uploaded file as a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio_path = temp_audio.name
                temp_audio.write(uploaded_file.read())

            try:
                # Load the audio file directly using Whisper
                audio = whisper.load_audio(temp_audio_path)
                audio = whisper.pad_or_trim(audio)
                mel = whisper.log_mel_spectrogram(audio).to(model.device)

                # Detect language
                _, probs = model.detect_language(mel)
                detected_lang = max(probs, key=probs.get)

                # Transcribe
                result = model.transcribe(temp_audio_path)
                transcription_text = result["text"]
                
                st.success(f"Detected Language: {detected_lang.upper()}")
                st.text_area("Transcription", transcription_text, height=200)

                # Create a temporary text file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_txt:
                    temp_txt_path = temp_txt.name
                    temp_txt.write(transcription_text.encode("utf-8"))
                    temp_txt.flush()

                # Provide download button
                with open(temp_txt_path, "rb") as f:
                    st.download_button(
                        label="Download Transcription",
                        data=f,
                        file_name="transcription.txt",
                        mime="text/plain"
                    )

            finally:
                # Cleanup temporary files
                os.remove(temp_audio_path)
                if 'temp_txt_path' in locals():
                    os.remove(temp_txt_path)
