import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.ai_blog_to_podcast_agent.config import (
    DEFAULT_MODEL,
    DEFAULT_VOICE,
    MODEL_OPTIONS,
)
from agents.ai_blog_to_podcast_agent.services.workflow import create_podcast_from_blog


st.set_page_config(page_title="Local Blog to Podcast", page_icon="🎙️")
st.title("Local Blog to Podcast Agent")

st.sidebar.header("Local Settings")
model_id = st.sidebar.selectbox(
    "Ollama model",
    MODEL_OPTIONS,
    index=MODEL_OPTIONS.index(DEFAULT_MODEL),
    help="llama3.2 is the lightest installed option on this machine. mistral is stronger but heavier.",
)
voice = st.sidebar.text_input("Piper voice", DEFAULT_VOICE)

st.sidebar.caption(
    "The Agno agent scrapes and writes the podcast script. Piper turns that script into local WAV audio."
)

url = st.text_input("Enter blog URL:", "")

if st.button("Generate Podcast"):
    if not url.strip():
        st.warning("Please enter a blog URL")
    else:
        try:
            with st.spinner(f"Creating podcast with {model_id}..."):
                result = create_podcast_from_blog(url.strip(), model_id, voice)

            st.success("Podcast generated!")
            st.audio(result.audio_bytes, format=result.audio_format)

            st.download_button(
                "Download Podcast",
                result.audio_bytes,
                result.filename,
                result.audio_format,
            )

            with st.expander("Podcast Script"):
                st.write(result.script)
        except Exception as error:
            st.error(str(error))
