from agents.ai_blog_to_podcast_agent.config import INSTALL_COMMAND
from shared.dependencies import missing_dependency_message


def scrape_blog(url: str) -> str:
    """Extract readable article text from a blog URL."""
    try:
        import trafilatura
    except ModuleNotFoundError as error:
        raise RuntimeError(missing_dependency_message(error, INSTALL_COMMAND)) from error

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise RuntimeError("Could not download the blog URL. Try a public article page.")

    article_text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        output_format="txt",
    )

    if not article_text:
        raise RuntimeError(
            "Could not extract readable article text. A JavaScript-heavy page may need Crawl4AI later."
        )

    return article_text.strip()
