import re

from agents.ai_blog_to_podcast_agent.config import (
    DEFAULT_SCRIPT_LIMIT,
    INSTALL_COMMAND,
)
from agents.ai_blog_to_podcast_agent.tools.scrape_tools import build_current_blog_scrape_tool
from shared.dependencies import missing_dependency_message


def clean_podcast_script(script: str) -> str:
    cleaned = script.strip()
    cleaned = re.sub(
        r"^(here('| i)s|here is)\s+(a\s+possible\s+|a\s+conversational\s+|a\s+|the\s+)?"
        r"podcast script(?:\s+based\s+on\s+the\s+(?:article|blog|blog text))?[^:\n]*:?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip()

    return cleaned.strip('"').strip()


def create_blog_to_podcast_agent(model_id: str, url: str):
    try:
        from agno.agent import Agent
        from agno.models.ollama import Ollama
    except ModuleNotFoundError as error:
        raise RuntimeError(missing_dependency_message(error, INSTALL_COMMAND)) from error

    scrape_current_blog = build_current_blog_scrape_tool(url)

    return Agent(
        name="Local Blog to Podcast Agent",
        model=Ollama(id=model_id),
        tools=[scrape_current_blog],
        instructions=[
            "You convert blog URLs into short podcast scripts.",
            "First call the scrape_current_blog tool. It takes no arguments.",
            "Use the scraped article text to write a conversational podcast script.",
            "Start directly with the podcast narration, as if the host is already speaking.",
            "Never start with phrases like 'Here is', 'Here's', 'This is', or 'Based on the article'.",
            f"Keep the script under {DEFAULT_SCRIPT_LIMIT} characters.",
            "Do not mention tool usage, scraping, summaries, or implementation details.",
            "Return only the final podcast script text.",
        ],
    )


def generate_podcast_script(url: str, model_id: str) -> str:
    agent = create_blog_to_podcast_agent(model_id, url)
    prompt = f"Scrape and summarize this blog for a podcast: {url}"
    response = agent.run(prompt)
    script = response.content if hasattr(response, "content") else str(response)

    if not script:
        raise RuntimeError("The local model did not return a podcast script.")

    return clean_podcast_script(script)
