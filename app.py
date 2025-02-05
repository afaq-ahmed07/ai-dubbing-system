import streamlit as st
import os
from whisper_utils import load_whisper_model, transcribe_audio
from file_utils import save_audio_temp, extract_audio_from_video
from ui_components import get_user_input

# Load Whisper model
model = load_whisper_model()

st.title("Whisper AI Local Transcription")

# Get user input (audio/video)
audio_data, video_data = get_user_input()

if audio_data or video_data:
    if st.button("Transcribe"):
        with st.spinner("Processing..."):
            audio_path = None
            txt_path = None
            srt_path = None
            try:
                # If video file is provided, extract audio
                if video_data:
                    audio_path = extract_audio_from_video(video_data)
                else:
                    audio_path = save_audio_temp(audio_data)
                
                # Transcribe using Whisper
                detected_lang, transcription_text, srt_content = transcribe_audio(model, audio_path)

                # Handle cases where transcription failed
                if not transcription_text:
                    st.error("Failed to transcribe audio. Please try again with a different file.")
                    raise Exception("Transcription failed.")

                st.success(f"Detected Language: {detected_lang.upper()}")
                st.text_area("Transcription", transcription_text, height=200)

                # Save transcription to files
                txt_path = audio_path.replace(".wav", ".txt")
                srt_path = audio_path.replace(".wav", ".srt")

                with open(txt_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(transcription_text)

                with open(srt_path, "w", encoding="utf-8") as srt_file:
                    srt_file.write(srt_content)

                # Provide download buttons
                with open(txt_path, "rb") as f_txt:
                    st.download_button("Download Transcription (TXT)", f_txt, file_name="transcription.txt", mime="text/plain")

                with open(srt_path, "rb") as f_srt:
                    st.download_button("Download Subtitles (SRT)", f_srt, file_name="subtitles.srt", mime="text/srt")

            except Exception as e:
                st.error(f"An error occurred: {e}")

            finally:
                # Cleanup temporary files safely
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)
                if txt_path and os.path.exists(txt_path):
                    os.remove(txt_path)
                if srt_path and os.path.exists(srt_path):
                    os.remove(srt_path)
