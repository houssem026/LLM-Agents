import unittest

from agents.ai_blog_to_podcast_agent.services.workflow import PodcastResult


class WorkflowTests(unittest.TestCase):
    def test_podcast_result_defaults_to_wav_download(self):
        result = PodcastResult(script="hello", audio_bytes=b"wav")

        self.assertEqual(result.audio_format, "audio/wav")
        self.assertEqual(result.filename, "podcast.wav")


if __name__ == "__main__":
    unittest.main()
