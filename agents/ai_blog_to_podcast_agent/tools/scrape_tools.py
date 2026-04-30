from typing import Any

from agno.tools import tool

from agents.ai_blog_to_podcast_agent.config import MAX_ARTICLE_CHARS
from agents.ai_blog_to_podcast_agent.services.scraper import scrape_blog


def normalize_tool_url(url: Any) -> str:
    if isinstance(url, str):
        return url

    if isinstance(url, dict):
        for key in ("url", "value", "text", "type"):
            value = url.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                return value

    raise ValueError(f"Expected a URL string, got: {url!r}")


@tool(
    name="scrape_blog",
    description="Scrape a blog URL and return clean readable article text.",
    instructions="Use this tool whenever the user asks to scrape, read, or summarize a blog URL.",
)
def scrape_blog_tool(url: Any) -> str:
    """Scrape a blog URL and return clean article text."""
    article_text = scrape_blog(normalize_tool_url(url))
    return article_text[:MAX_ARTICLE_CHARS]


def build_current_blog_scrape_tool(url: str):
    """Build a no-argument scraper tool bound to one URL.

    Small local models can struggle to pass tool arguments exactly. Binding the
    URL in Python keeps the agentic workflow while removing that brittle step.
    """

    bound_url = url

    @tool(
        name="scrape_current_blog",
        description="Scrape the current blog URL and return clean readable article text.",
        instructions="Call this tool first. It takes no arguments.",
    )
    def scrape_current_blog(urls: Any = None, url: Any = None, **kwargs: Any) -> str:
        article_text = scrape_blog(bound_url)
        return article_text[:MAX_ARTICLE_CHARS]

    return scrape_current_blog
