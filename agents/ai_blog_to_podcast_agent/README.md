# AI Blog to Podcast Agent

Local-first agent workspace that turns a public blog URL into a short podcast episode. It extracts readable article text, asks a local LLM to write a conversational script, then renders the script as WAV audio.

## Architecture

```text
Streamlit UI
    |
    v
services.workflow.create_podcast_from_blog
    |
    +--> services.podcast_agent.generate_podcast_script
    |       |
    |       +--> Agno Agent
    |              |
    |              +--> Ollama local model
    |              +--> scrape_current_blog tool
    |                     |
    |                     +--> trafilatura article extraction
    |
    +--> services.tts.text_to_speech
            |
            +--> Piper CLI local text-to-speech
```

The code is split by responsibility:

- `blog_to_podcast.py`: Streamlit app entrypoint and user controls.
- `services/workflow.py`: orchestration layer that returns a `PodcastResult`.
- `services/podcast_agent.py`: Agno agent construction, prompting, and script cleanup.
- `tools/scrape_tools.py`: Agno-compatible scraping tools.
- `services/scraper.py`: article extraction with `trafilatura`.
- `services/tts.py`: WAV generation through the local Piper CLI.
- `config.py`: model, voice, article length, and install defaults.

## Technical Choices

### Agent Framework: Agno

The agent uses `agno` because it provides a compact Python interface for model-backed agents and tools. The scraping step is exposed as an Agno tool, so the LLM can follow an explicit "scrape first, write second" workflow instead of receiving hidden preprocessed text.

The current implementation binds the requested URL into a no-argument `scrape_current_blog` tool. This keeps the workflow agentic while avoiding brittle tool argument formatting from smaller local models.

### LLM Runtime: Ollama

The script-generation model runs locally through Ollama:

- Default model: `llama3.2`
- Optional model: `mistral`

`llama3.2` is the default because it is lighter and suitable for local development. `mistral` is available as a stronger but heavier option when the machine can afford the extra latency and memory.

The model is instructed to return only the final podcast script, stay under `DEFAULT_SCRIPT_LIMIT`, and avoid implementation details such as scraping or tool usage.

### Article Extraction: trafilatura

`trafilatura` handles fetching and extracting readable article text from public blog pages. It removes comments and tables and returns plain text, which keeps the LLM input focused on article content.

The extracted article is capped with `MAX_ARTICLE_CHARS` before being passed back through the tool. This protects local context windows and keeps generation latency predictable.

### Text-to-Speech: Piper

Audio is generated locally with the Piper CLI. The default voice is:

- `en_US-lessac-medium`

Voice files live under `voices/`, and the app returns `audio/wav` bytes with a default `podcast.wav` filename.

### UI Framework: Streamlit

Streamlit is used for the app shell because it is simple for local agent demos: URL input, model selection, voice configuration, audio playback, download, and script inspection are all handled in one Python file.

## Setup

Install Python dependencies from the repository root:

```bash
pip install -r agents/ai_blog_to_podcast_agent/requirements.txt
```

Install the Ollama models used by the app:

```bash
ollama pull llama3.2
ollama pull mistral
```

Download the default Piper voice:

```bash
python3 -m piper.download_voices --download-dir agents/ai_blog_to_podcast_agent/voices en_US-lessac-medium
```

## Run

From the repository root:

```bash
streamlit run agents/ai_blog_to_podcast_agent/blog_to_podcast.py
```

Enter a public blog URL, choose an Ollama model, and generate the podcast. The app will display an audio player, a WAV download button, and the generated script.

## Tests

Run the focused unit tests from the repository root:

```bash
python3 -m unittest discover agents/ai_blog_to_podcast_agent/tests
```

The tests cover result defaults, script cleanup, URL normalization, and the bound scraper tool shape.

## Current Limitations

- JavaScript-heavy pages may fail extraction because `trafilatura` works best on server-rendered article pages.
- The app expects Ollama, the selected model, Piper, and the selected voice files to be installed locally.
- Generated script quality depends on the selected local model and the quality of extracted article text.
