```markdown
### AI Video Dubbing System 🎥🔊

An automated pipeline to transcribe, translate, and dub videos using cutting-edge AI tools.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

![Demo](docs/demo.gif) *Replace with your actual demo GIF*

## ✨ Features
- Extract audio from video (MP4, MOV, AVI)
- Generate transcriptions with OpenAI Whisper
- Translate text to 100+ languages using GoogleTrans
- Create dubbed voiceovers with Play.ht
- Merge audio/video with MoviePy
- Download SRT subtitle files

## ⚙️ Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/ai-dubbing-system.git
cd ai-dubbing-system
```

2. **Install System Dependencies**
```bash
# For Ubuntu/Debian
sudo apt-get install ffmpeg

# For macOS
brew install ffmpeg
```

3. **Install Python Packages**
```bash
pip install -r requirements.txt
```

## 🚀 Usage
1. Place input videos in `/input_videos`
2. Run main script:
```bash
python main.py
```
3. Follow prompts to:
   - Select input video
   - Choose target language
   - Select voice profile
4. Find results in `/output`:
   - Dubbed video (MP4)
   - Transcript (TXT)
   - Subtitles (SRT)

## 📝 Notes
- First-time Whisper model download (~1.5GB)
- Play.ht voices cost credits (free tier available)
- Supported video formats: MP4, MOV, AVI

## 🤝 Contributing
Pull requests welcome! For major changes, open an issue first.
