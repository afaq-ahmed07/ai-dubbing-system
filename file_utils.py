import tempfile
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip,CompositeVideoClip
import os
import streamlit as st

def save_audio_temp(audio_bytes):
    """Save audio bytes to a temporary file and return its path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
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

def replace_audio_in_video(video_data, dubbed_audio_buffer):
    """
    Replaces the original audio of a video with the dubbed audio.
    
    Parameters:
      video_data (bytes): Binary data of the input video file.
      dubbed_audio_buffer (BytesIO): In-memory buffer containing the dubbed audio data.
    
    Returns:
      bytes: The final video's data in bytes.
    """
    # Write the video binary data to a temporary file.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(video_data)
        temp_video_path = temp_video_file.name

    # Write the dubbed audio data (BytesIO) to a temporary file.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(dubbed_audio_buffer.getvalue())
        temp_audio_path = temp_audio_file.name

    # Create a temporary file for the output video.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output_file:
        output_video_path = temp_output_file.name

    # Load the video and the dubbed audio using MoviePy.
    video = VideoFileClip(temp_video_path)
    dubbed_audio = AudioFileClip(temp_audio_path)
    
    new_audioclip = CompositeAudioClip([dubbed_audio])
    
    # Set the new dubbed audio as the video's audio.
    video.audio = new_audioclip
    
    # Write the final video to the temporary output file.
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    
    # Read the output video into memory.
    with open(output_video_path, "rb") as f:
        video_bytes = f.read()
    
    # Cleanup all temporary files.
    os.remove(temp_audio_path)
    os.remove(temp_video_path)
    os.remove(output_video_path)
    
    return video_bytes

