import whisper
import os

def load_whisper_model():
    """Load Whisper model."""
    return whisper.load_model("small")  # Options: tiny, base, small, medium, large

def format_timestamp_srt(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    milliseconds = int(round(seconds * 1000))
    hours = milliseconds // 3600000
    milliseconds %= 3600000
    minutes = milliseconds // 60000
    milliseconds %= 60000
    secs = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def transcribe_audio(model, audio_path):
    """Transcribe audio file using Whisper."""
    try:
        # Load and preprocess audio
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Detect language properly
        _, probs = model.detect_language(mel)
        detected_lang = max(probs, key=probs.get)

        # Transcribe
        result = model.transcribe(audio_path)
        transcription_text = result["text"]

        # Generate SRT content
        srt_lines = []
        for i, segment in enumerate(result.get("segments", []), start=1):
            start_ts = format_timestamp_srt(segment["start"])
            end_ts = format_timestamp_srt(segment["end"])
            text = segment["text"].strip()
            srt_lines.append(f"{i}\n{start_ts} --> {end_ts}\n{text}\n")

        srt_content = "\n".join(srt_lines)
        return detected_lang, transcription_text, srt_content
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None, None, None  # Return None to prevent further issues
