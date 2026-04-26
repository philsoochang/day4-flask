import io
import os
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import seed


class RenderSeedBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "render_seed.db")
        os.environ["DB_PATH"] = self.db_path

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        os.environ.pop("DB_PATH", None)
        self.temp_dir.cleanup()

    @patch("seed.fetch_news_items")
    def test_seed_news_posts_safe_prints_added_count_when_success(self, mock_fetch_news_items):
        mock_fetch_news_items.return_value = [
            {
                "title": "렌더 뉴스 1",
                "summary": "요약 1",
                "link": "https://example.com/1",
                "published": "Sun, 26 Apr 2026 10:00:00 +0900",
            }
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            added = seed.seed_news_posts_safe(limit=10)

        self.assertEqual(added, 1)
        self.assertIn("[seed] 1건 추가됨", output.getvalue())

    @patch("seed.fetch_news_items", side_effect=RuntimeError("rss error"))
    def test_seed_news_posts_safe_does_not_raise_on_failure(self, _mock_fetch_news_items):
        output = io.StringIO()
        with redirect_stdout(output):
            added = seed.seed_news_posts_safe(limit=10)

        self.assertEqual(added, 0)
        self.assertIn("[seed] 실패", output.getvalue())


if __name__ == "__main__":
    unittest.main()
