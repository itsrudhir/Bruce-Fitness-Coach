# 💪 Bruce Fitness Coach – Voice-Based AI Fitness Assistant

[![Streamlit App](https://img.shields.io/badge/Live%20App-Click%20Here-brightgreen?style=for-the-badge)](https://my-gym-coach.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-itsrudhir/Bruce--Fitness--Coach-blue?style=for-the-badge&logo=github)](https://github.com/itsrudhir/Bruce-Fitness-Coach)

**Bruce Fitness Coach** is a smart and interactive **AI fitness assistant** that helps users manage workouts, set goals, and receive personalized fitness advice using voice and text. Built with **Streamlit** and powered by **Groq's LLM**, this app brings a conversational gym coach right to your browser.

---

## 🌟 Features

- 🗣️ **Voice & Text Chat**: Converse with your coach by speaking or typing.
- 🧠 **Memory & Context**: Persistent memory that recalls past conversations.
- 🏋️ **Workout Logging**: Log workouts with type, duration, and notes.
- 📊 **History Tracking**: View and reflect on your fitness progress.
- 👤 **Profile Setup**: Customize your age, weight, and fitness goal.
- 🔄 **Memory Reset**: One-click option to clear all saved conversations.

---

## 🚀 Live Demo

👉 Try the app here: [https://my-gym-coach.streamlit.app](https://my-gym-coach.streamlit.app)

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) – UI framework for fast app prototyping
- [Groq](https://groq.com) – LLM backend for chat
- [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/) – Converts coach's replies to audio
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) – Transcribes user's voice queries
- [audio-recorder-streamlit](https://github.com/girishvs/streamlit-audio-recorder) – Mic integration in-browser

---

## 📦 Installation Guide

```bash
git clone https://github.com/itsrudhir/Bruce-Fitness-Coach.git
cd Bruce-Fitness-Coach
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
