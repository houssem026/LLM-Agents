import subprocess
import tempfile

from agents.ai_blog_to_podcast_agent.config import DEFAULT_VOICE, VOICES_DIR


def text_to_speech(script: str, voice: str = DEFAULT_VOICE) -> bytes:
    """Generate WAV audio bytes with the local Piper CLI."""
    with tempfile.NamedTemporaryFile(suffix=".wav") as audio_file:
        command = [
            "piper",
            "--model",
            voice,
            "--data-dir",
            str(VOICES_DIR),
            "--output_file",
            audio_file.name,
        ]
        result = subprocess.run(
            command,
            input=script,
            text=True,
            capture_output=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Piper failed to generate audio. "
                "Make sure the voice is downloaded with: "
                "`python3 -m piper.download_voices --download-dir "
                "agents/ai_blog_to_podcast_agent/voices en_US-lessac-medium`\n\n"
                f"{result.stderr.strip()}"
            )

        audio_file.seek(0)
        return audio_file.read()
