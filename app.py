import streamlit as st
import whisper
import tempfile
import os
from audio_recorder_streamlit import audio_recorder
from moviepy import VideoFileClip  # Used to extract audio from video

# Load the Whisper model once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")  # Options: "tiny", "base", "small", "medium", "large"

model = load_whisper_model()

st.title("Whisper AI Local Transcription")

# Let user choose input method
input_method = st.radio("Select Input Method", ("Upload Audio File", "Record Audio", "Upload Video File"))

audio_data = None
temp_video_path = None  # To store temporary video file path if needed
temp_audio_video_path = None  # For audio extracted from video

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
elif input_method == "Upload Video File":
    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    if video_file is not None:
        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video_path = temp_video.name
            temp_video.write(video_file.read())
        st.write("Extracting audio from video...")
        try:
            # Use MoviePy to extract audio from the video file
            clip = VideoFileClip(temp_video_path)
            # Save the extracted audio to a temporary file in WAV format
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_video:
                temp_audio_video_path = temp_audio_video.name
            clip.audio.write_audiofile(temp_audio_video_path, logger=None)
            # Read the extracted audio data
            with open(temp_audio_video_path, "rb") as f:
                audio_data = f.read()
            st.audio(audio_data, format="audio/wav")
        except Exception as e:
            st.error(f"Error extracting audio: {e}")

def format_timestamp_srt(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    milliseconds = int(round(seconds * 1000))
    hours = milliseconds // 3600000
    milliseconds -= hours * 3600000
    minutes = milliseconds // 60000
    milliseconds -= minutes * 60000
    secs = milliseconds // 1000
    milliseconds -= secs * 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

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

                # --- Create TXT file ---
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_txt:
                    temp_txt_path = temp_txt.name
                    temp_txt.write(transcription_text.encode("utf-8"))
                    temp_txt.flush()

                # --- Generate SRT file from segments ---
                srt_lines = []
                for i, segment in enumerate(result.get("segments", []), start=1):
                    start_ts = format_timestamp_srt(segment["start"])
                    end_ts = format_timestamp_srt(segment["end"])
                    # Remove any extraneous whitespace from the segment text
                    text = segment["text"].strip()
                    srt_lines.append(f"{i}\n{start_ts} --> {end_ts}\n{text}\n")
                srt_content = "\n".join(srt_lines)

                # Save SRT content to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as temp_srt:
                    temp_srt_path = temp_srt.name
                    temp_srt.write(srt_content.encode("utf-8"))
                    temp_srt.flush()

                # Provide download button for TXT file
                with open(temp_txt_path, "rb") as f_txt:
                    st.download_button(
                        label="Download Transcription (TXT)",
                        data=f_txt,
                        file_name="transcription.txt",
                        mime="text/plain"
                    )

                # Provide download button for SRT file
                with open(temp_srt_path, "rb") as f_srt:
                    st.download_button(
                        label="Download Subtitles (SRT)",
                        data=f_srt,
                        file_name="subtitles.srt",
                        mime="text/srt"
                    )
            finally:
                # Clean up temporary files
                os.remove(temp_audio_path)
                if 'temp_txt_path' in locals():
                    os.remove(temp_txt_path)
                if 'temp_srt_path' in locals():
                    os.remove(temp_srt_path)
                # Clean up video/audio extraction temporary files if they exist
                if temp_video_path is not None and os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                if temp_audio_video_path is not None and os.path.exists(temp_audio_video_path):
                    os.remove(temp_audio_video_path)