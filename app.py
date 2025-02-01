import streamlit as st
import whisper

# Load Whisper model once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")  # Use "small", "medium", or "large" if needed

model = load_whisper_model()

st.title("Whisper AI Local Transcription")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            # Load and process audio
            audio = whisper.load_audio(audio_wav)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)

            # Detect language
            _, probs = model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)

            # Transcribe
            options = whisper.DecodingOptions()
            result = whisper.decode(model, mel, options)

            st.success(f"Detected Language: {detected_lang.upper()}")
            st.text_area("Transcription", result.text, height=200)
