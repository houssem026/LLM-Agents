from pathlib import Path


AGENT_DIR = Path(__file__).parent
VOICES_DIR = AGENT_DIR / "voices"

DEFAULT_MODEL = "llama3.2"
MODEL_OPTIONS = ["llama3.2", "mistral"]

DEFAULT_VOICE = "en_US-lessac-medium"
DEFAULT_SCRIPT_LIMIT = 1800
MAX_ARTICLE_CHARS = 12000

INSTALL_COMMAND = "pip install -r agents/ai_blog_to_podcast_agent/requirements.txt"
