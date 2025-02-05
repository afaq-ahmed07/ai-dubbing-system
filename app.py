import streamlit as st
import os
from pyht import Client
from pyht.client import TTSOptions
from whisper_utils import load_whisper_model, transcribe_audio
from file_utils import save_audio_temp, extract_audio_from_video
from ui_components import get_user_input
from translate_utils import get_supported_languages, translate_text
from pyht  import Language # Import Language
import io


# Load Whisper model
model = load_whisper_model()
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

# Session state to store intermediate results
if "transcription_text" not in st.session_state:
    st.session_state.transcription_text = None
if "translated_text" not in st.session_state:
    st.session_state.translated_text = None


def text_to_speech_playht(text):
    """Generate speech from text using Play.ht streaming API via pyht."""
    # Initialize the Play.ht client
    print("entered function")
    client = Client(
        user_id="71n2353Y66cvZ1YxfVaooM5dGAx2",  # Replace with your actual Play.ht User ID
        api_key="b59821992ba64324af0821e2c90717bd",  # Replace with your actual Play.ht API Key
    )
    # Set TTS options
    options = TTSOptions(voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json",language=Language.URDU)  # Ensure the language is in uppercase)

    try:
        # Create a BytesIO object to hold the audio data in memory
        audio_buffer = io.BytesIO()
        
        # Stream the audio chunks and write them to the buffer
        for chunk in client.tts(text, options):
            audio_buffer.write(chunk)
        
        # Move back to the start of the BytesIO buffer so it can be read later
        audio_buffer.seek(0)
        
        return audio_buffer  # Return the in-memory audio data

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def handle_translation():
    """Handles the translation process and stores the translated text in session state."""
    if not st.session_state.transcription_text:
        st.warning("Please transcribe the audio first.")
        return

    st.markdown("### Translate Transcription")
    supported_langs = get_supported_languages()

    lang_options = {name.title(): code for code, name in supported_langs.items()}
    default_lang = "Urdu" if "Urdu" in lang_options else None

    selected_lang = st.selectbox("Select target language", sorted(lang_options.keys()),
                                 index=list(lang_options.keys()).index(default_lang) if default_lang else 0)

    if st.button("Translate"):
        with st.spinner("Translating..."):
            target_lang_code = lang_options[selected_lang]
            st.session_state.translated_text = translate_text(st.session_state.transcription_text, target_lang_code)
            st.success(f"Translated to {selected_lang}:")
            st.text_area("Translated Text", st.session_state.translated_text, height=200)

def generate_voiceover():
    """Generates a voiceover from translated text."""
    if not st.session_state.translated_text:
        st.warning("Please translate the text first.")
        return

    st.markdown("### Generate Voiceover")
    with st.spinner("Generating voiceover..."):
        audio_data = text_to_speech_playht(st.session_state.translated_text)
        if audio_data:
            st.success("Voiceover Generated Successfully!")
            st.audio(audio_data, format="audio/mp3")
            st.download_button(
                "Download Audio",
                data=audio_data,
                file_name="voiceover.mp3",
                mime="audio/mp3"
            )
    st.stop()

# Streamlit UI
st.title("AI Dubbing System")

# Get user input (audio/video)
audio_data, video_data = get_user_input()

if audio_data or video_data:
    if st.button("Transcribe"):
        with st.spinner("Processing..."):
            audio_path = None
            try:
                # If video file is provided, extract audio; otherwise, save the audio bytes
                if video_data:
                    audio_path = extract_audio_from_video(video_data)
                else:
                    audio_path = save_audio_temp(audio_data)

                # Transcribe using Whisper
                detected_lang, transcription_text, srt_content = transcribe_audio(model, audio_path)

                if not transcription_text:
                    st.error("Failed to transcribe audio. Please try again with a different file.")
                    raise Exception("Transcription failed.")

                st.success(f"Detected Language: {detected_lang.upper()}")
                st.session_state.transcription_text = transcription_text
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



            except Exception as e:
                st.error(f"An error occurred: {e}")

            finally:
                # Cleanup temporary files
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)

# Section for translation
if st.session_state.transcription_text:
    handle_translation()

# Section for generating voiceover
if st.session_state.translated_text:
    generate_voiceover()
