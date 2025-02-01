# Whisper_Audio_Transcription 🎙️

A simple **Streamlit web app** that uses **Whisper AI** to transcribe audio files **locally** (without OpenAI's API).  

![Streamlit Whisper AI](https://streamlit.io/images/brand/streamlit-mark-light.svg)  

---

## 🚀 Features  
✅ Upload audio files (**MP3, WAV, FLAC, M4A**)  
✅ Automatically detects language 🏳️  
✅ Converts speech to text using **Whisper AI**  
✅ Runs **locally** without using OpenAI's API  
✅ Simple and fast UI using **Streamlit**  


---

## 🛠️ Installation & Usage  

### 1️⃣ Deploy on Streamlit Cloud (No Installation Needed)  
1. Fork this repo and push it to **GitHub**  
2. Go to **[Streamlit Cloud](https://share.streamlit.io/)**  
3. Click **"Deploy an app"** → Select your GitHub repo  
4. Set the main file to **`app.py`**  
5. Click **Deploy** and get a public link 🎉  

---

### 2️⃣ Run Locally (Requires Installation)  

#### 🔹 Step 1: Clone the Repository  
```bash
git clone https://github.com/your-username/Whisper_Audio_Transcription.git
cd Whisper_Audio_Transcription
pip install -r requirements.txt
streamlit run app.py


