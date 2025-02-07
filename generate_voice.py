from pyht  import Language # Import Language
import io
from pyht import Client
from pyht.client import TTSOptions
import streamlit as st

def text_to_speech_playht(text):
    """Generate speech from text using Play.ht streaming API via pyht."""
    # Initialize the Play.ht client
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