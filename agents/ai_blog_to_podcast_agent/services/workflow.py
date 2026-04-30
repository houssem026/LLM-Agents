from dataclasses import dataclass

from agents.ai_blog_to_podcast_agent.config import DEFAULT_VOICE
from agents.ai_blog_to_podcast_agent.services.podcast_agent import generate_podcast_script
from agents.ai_blog_to_podcast_agent.services.tts import text_to_speech


@dataclass(frozen=True)
class PodcastResult:
    script: str
    audio_bytes: bytes
    audio_format: str = "audio/wav"
    filename: str = "podcast.wav"


def create_podcast_from_blog(
    url: str,
    model_id: str,
    voice: str = DEFAULT_VOICE,
) -> PodcastResult:
    script = generate_podcast_script(url, model_id)
    audio_bytes = text_to_speech(script, voice)

    return PodcastResult(script=script, audio_bytes=audio_bytes)
