import streamlit as st
from groq import Groq
import json, os
import speech_recognition as sr
from gtts import gTTS
import io
from audio_recorder_streamlit import audio_recorder

# --- Configuration ---
GROQ_API_KEY = st.secrets['GROQ_API_KEY']  # Use Streamlit Cloud secrets for secure API keys
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"
MEMORY_FILE = "fitness_memory.json"
WORKOUT_LOG = "workout_log.json"

# --- Helpers for persistence ---
def load_json(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except json.JSONDecodeError:
            st.warning(f"Error reading {path}. Initializing with default data.")
            return default
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

# --- Streamlit Setup ---
st.set_page_config(page_title="Fitness Assistant", layout="wide")
st.title("💪 Fitness Assistant with Voice & Memory")

# Load or init memory and logs
if "messages" not in st.session_state:
    st.session_state.messages = load_json(MEMORY_FILE, [])
if "workouts" not in st.session_state:
    st.session_state.workouts = load_json(WORKOUT_LOG, [])

# Sidebar: user profile and goals
st.sidebar.header("Your Profile & Goals")
with st.sidebar.form("profile_form", clear_on_submit=False):
    if "profile" not in st.session_state:
        st.session_state.profile = load_json("profile.json", {"age": 25, "weight": 70, "goal": "Maintain fitness"})
    age = st.number_input("Age", value=st.session_state.profile["age"], min_value=10, max_value=100)
    weight = st.number_input("Weight (kg)", value=st.session_state.profile["weight"], min_value=30, max_value=200)
    goal = st.text_input("Goal", value=st.session_state.profile["goal"])
    if st.form_submit_button("Save Profile"):
        st.session_state.profile = {"age": age, "weight": weight, "goal": goal}
        save_json("profile.json", st.session_state.profile)
        st.success("Profile saved.")

# Tabs for functionality
tabs = st.tabs(["Chat Coach", "Log Workout", "View Workouts"])

# --- Tab 1: Chat Coach ---
with tabs[0]:
    st.subheader("🗣️ Voice & Text Coaching")
    for m in st.session_state.messages:
        who = "You" if m["role"] == "user" else "Coach"
        st.markdown(f"**{who}:** {m['content']}")

    audio_bytes = audio_recorder("Record question", "Stop recording")
    user_voice = None
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with open("input.wav", "wb") as f:
            f.write(audio_bytes)
        r = sr.Recognizer()
        with sr.AudioFile("input.wav") as src:
            audio = r.record(src)
        try:
            user_voice = r.recognize_google(audio)
            st.markdown(f"**You (voice):** {user_voice}")
        except Exception:
            st.error("Could not transcribe voice.")

    with st.form("chat_form", clear_on_submit=True):
        txt = st.text_input("Or type your question to your fitness coach:")
        submit = st.form_submit_button("Send")

    query = user_voice or (txt if submit and txt else None)
    if query:
        if not any(m["role"] == "system" for m in st.session_state.messages):
            st.session_state.messages.insert(0, {"role": "system", "content": "You are a helpful fitness coach. Provide personalized workouts, nutrition tips, and motivation. Don't give too lengthy messages. Keep responses relevant to the user's query. Do not respond to anything other than fitness and nutrition advice."})
        st.session_state.messages.append({"role": "user", "content": query})
        with st.spinner("Coach is thinking…"):
            resp = client.chat.completions.create(
                messages=st.session_state.messages,
                model=MODEL_NAME, stream=False
            )
        reply = resp.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_json(MEMORY_FILE, st.session_state.messages)

        st.markdown(f"**Coach:** {reply}")
        # TTS with gTTS
        try:
            tts = gTTS(text=reply)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            st.audio(buf, format="audio/mp3")
        except Exception as e:
            st.error(f"Error with TTS: {e}")

# --- Tab 2: Log Workout ---
with tabs[1]:
    st.subheader("🏋️ Log a Workout")
    with st.form("log_form", clear_on_submit=True):
        date = st.date_input("Date")
        wtype = st.selectbox("Type", ["Cardio", "Strength", "Flexibility", "Balance"])
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=300)
        notes = st.text_area("Notes (exercises, intensity)")
        if st.form_submit_button("Add Workout"):
            entry = {"date": date.isoformat(), "type": wtype, "duration": duration, "notes": notes}
            st.session_state.workouts.append(entry)
            save_json(WORKOUT_LOG, st.session_state.workouts)
            st.success("Workout logged!")

# --- Tab 3: View Workouts ---
with tabs[2]:
    st.subheader("📊 Your Workout History")
    if st.session_state.workouts:
        for e in st.session_state.workouts:
            st.markdown(f"- **{e['date']}** | {e['type']} for {e['duration']} min — {e['notes']}")
    else:
        st.info("No workouts logged yet.")

# Sidebar instructions
st.sidebar.markdown('''
This fitness assistant:  
• Chat with your AI coach via voice or text.  
• Log workouts and view history.  
• Profile & goals persist across sessions.  
)
