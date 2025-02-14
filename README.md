# AI Dubbing System

A Streamlit-based AI dubbing system that allows you to:
- Upload or record audio/video.
- Transcribe audio using OpenAI's Whisper.
- Translate the transcription into a target language.
- Generate a dubbed voiceover using Play.ht Text-to-Speech.
- Replace the original audio in a video with the dubbed audio.
- Download the final dubbed video.

---

## Features

- **Multi-Input Support:**  
  Upload an audio file, record audio in real time, or upload a video file.

- **Speech-to-Text:**  
  Transcribe audio using OpenAI Whisper.

- **Translation:**  
  Translate the transcribed text into a selected language using Google Translate API.

- **Text-to-Speech:**  
  Generate a dubbed voiceover using the Play.ht API.  
  *Note: Users must enter their own Play.ht credentials (User ID and API Key) via the UI.*

- **Video Dub:**  
  Replace the original audio in the video with the dubbed audio and download the final video.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/afaq-ahmed07/ai-dubbing-system
   cd ai-dubbing-system
2. **Install Dependencies:**
    ```bash
   pip install -r requirements.txt
## Usage
1. **Obtain Play.ht Credentials:**
   * Sign up for a Play.ht account.
   * Retrieve your Play.ht User ID and API Key.
   * Enter these credentials in the app
2. **Run the App:**
   ```bash
   streamlit run app.py
## File Structure:
   /ai_dubbing_system
   │── app.py                # Main Streamlit application
   │── whisper_utils.py      # Functions to load the Whisper model and transcribe audio
   │── file_utils.py         # Functions for file handling and video processing (e.g., replacing audio)
   │── ui_components.py      # Custom UI components (e.g., input selection and styled radio buttons)
   │── translate_utils.py    # Functions for translating text using Google Translate API
   │── requirements.txt      # Project dependencies
   │── README.md             # This README file

