import os
import sys
import tempfile
import unittest
from unittest.mock import patch


class SeedStartupHookTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "startup_seed.db")
        os.environ["DB_PATH"] = self.db_path
        os.environ.pop("NEWS_SEED_ON_STARTUP", None)
        if "app" in sys.modules:
            del sys.modules["app"]

    def tearDown(self):
        os.environ.pop("DB_PATH", None)
        os.environ.pop("NEWS_SEED_ON_STARTUP", None)
        if "app" in sys.modules:
            del sys.modules["app"]
        self.temp_dir.cleanup()

    def test_app_import_calls_seed_news_on_startup_by_default(self):
        os.environ.pop("NEWS_SEED_ON_STARTUP", None)

        with patch("seed.seed_news_posts_safe", return_value=0) as mock_seed:
            import app  # noqa: F401

        self.assertEqual(mock_seed.call_count, 1)

    def test_app_import_skips_seed_news_when_disabled(self):
        os.environ["NEWS_SEED_ON_STARTUP"] = "0"

        with patch("seed.seed_news_posts_safe", return_value=0) as mock_seed:
            import app  # noqa: F401

        self.assertEqual(mock_seed.call_count, 0)


if __name__ == "__main__":
    unittest.main()
