import unittest

from agents.ai_blog_to_podcast_agent.tools.scrape_tools import (
    build_current_blog_scrape_tool,
    normalize_tool_url,
)


class ScrapeToolTests(unittest.TestCase):
    def test_normalize_tool_url_accepts_string(self):
        self.assertEqual(normalize_tool_url("https://example.com"), "https://example.com")

    def test_normalize_tool_url_accepts_local_model_dict_shape(self):
        self.assertEqual(
            normalize_tool_url({"type": "https://example.com"}),
            "https://example.com",
        )

    def test_bound_scrape_tool_has_no_argument_name(self):
        scrape_tool = build_current_blog_scrape_tool("https://example.com")

        self.assertEqual(scrape_tool.name, "scrape_current_blog")


if __name__ == "__main__":
    unittest.main()
