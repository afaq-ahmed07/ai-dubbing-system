import streamlit as st
import os
from whisper_utils import load_whisper_model, transcribe_audio
from file_utils import save_audio_temp, extract_audio_from_video
from ui_components import get_user_input
from translate_utils import get_supported_languages, translate_text

# Load Whisper model
model = load_whisper_model()

# Function to handle translation and display
# Function to handle translation and display
def handle_translation(transcription_text):
    """
    Handles the translation process and displays the translated text and download button.
    """
    st.markdown("### Translate Transcription")
    supported_langs = get_supported_languages()
                
    # Create a mapping for display: Language Name (Title Case) -> Language Code
    lang_options = {name.title(): code for code, name in supported_langs.items()}
    
    # Set Urdu as the default language if available
    default_lang = "Urdu" if "Urdu" in lang_options else None

    selected_lang = st.selectbox("Select target language", sorted(lang_options.keys()), index=list(lang_options.keys()).index(default_lang) if default_lang else 0)

    # Button to trigger translation
    if st.button("Translate Text"):
        target_lang_code = lang_options[selected_lang]
        with st.spinner("Translating..."):
            translated_text = translate_text(transcription_text, target_lang_code)
            st.success(f"Translation to {selected_lang}:")
            st.text_area("Translated Text", translated_text, height=200)
        
            # Provide a download button for the translated text
            st.download_button(
                "Download Translated Text",
                data=translated_text,
                file_name="translated.txt",
                mime="text/plain"
            )


st.title("Whisper AI Local Transcription & Translation")

# Get user input (audio/video)
audio_data, video_data = get_user_input()

if audio_data or video_data:
    if st.button("Transcribe"):
        with st.spinner("Processing..."):
            audio_path = None
            txt_path = None
            srt_path = None
            try:
                # If video file is provided, extract audio; otherwise, save the audio bytes
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

                # Provide download buttons for TXT and SRT files
                with open(txt_path, "rb") as f_txt:
                    st.download_button("Download Transcription (TXT)", f_txt, file_name="transcription.txt", mime="text/plain")
                with open(srt_path, "rb") as f_srt:
                    st.download_button("Download Subtitles (SRT)", f_srt, file_name="subtitles.srt", mime="text/srt")

                handle_translation(transcription_text)

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
