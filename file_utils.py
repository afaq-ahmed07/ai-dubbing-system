import tempfile
from moviepy import VideoFileClip

def save_audio_temp(audio_bytes):
    """Save audio bytes to a temporary file and return its path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        print(temp_audio.name)
        return temp_audio.name

def extract_audio_from_video(video_bytes):
    """Extract audio from an uploaded video file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_bytes)
        video_path = temp_video.name

    audio_path = video_path.replace(".mp4", ".wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    
    return audio_path
