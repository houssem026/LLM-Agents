import unittest

from agents.ai_blog_to_podcast_agent.services.podcast_agent import clean_podcast_script


class PodcastAgentTests(unittest.TestCase):
    def test_clean_podcast_script_removes_common_preface(self):
        script = "Here's a possible podcast script based on the blog text:\n\"Welcome back.\""

        self.assertEqual(clean_podcast_script(script), "Welcome back.")

    def test_clean_podcast_script_removes_article_preface_without_colon(self):
        script = "Here's a podcast script based on the article\nWelcome back."

        self.assertEqual(clean_podcast_script(script), "Welcome back.")


if __name__ == "__main__":
    unittest.main()
