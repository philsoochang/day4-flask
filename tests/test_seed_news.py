import io
import os
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import seed


class SeedNewsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "seed_news.db")

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE posts (
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

        os.environ["DB_PATH"] = self.db_path

    def tearDown(self):
        os.environ.pop("DB_PATH", None)
        self.temp_dir.cleanup()

    @patch("seed.fetch_news_items")
    def test_seed_news_inserts_only_new_titles(self, mock_fetch_news_items):
        mock_fetch_news_items.return_value = [
            {
                "title": "기사 A",
                "summary": "요약 A",
                "link": "https://example.com/a",
                "published": "Sun, 26 Apr 2026 09:00:00 +0900",
            },
            {
                "title": "기사 B",
                "summary": "요약 B",
                "link": "https://example.com/b",
                "published": "Sun, 26 Apr 2026 09:01:00 +0900",
            },
        ]

        seed.seed_news_posts(limit=10)

        conn = sqlite3.connect(self.db_path)
        rows = conn.execute("SELECT title, content, image FROM posts ORDER BY id").fetchall()
        conn.close()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "기사 A")
        self.assertEqual(rows[0][1], "요약 A")
        self.assertIsNone(rows[0][2])

    @patch("seed.fetch_news_items")
    def test_seed_news_skips_duplicate_titles(self, mock_fetch_news_items):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO posts (title, content, image) VALUES (?, ?, ?)",
            ("기사 A", "기존 본문", None),
        )
        conn.commit()
        conn.close()

        mock_fetch_news_items.return_value = [
            {
                "title": "기사 A",
                "summary": "새 요약 A",
                "link": "https://example.com/a",
                "published": "Sun, 26 Apr 2026 09:00:00 +0900",
            },
            {
                "title": "기사 C",
                "summary": "요약 C",
                "link": "https://example.com/c",
                "published": "Sun, 26 Apr 2026 09:02:00 +0900",
            },
        ]

        seed.seed_news_posts(limit=10)

        conn = sqlite3.connect(self.db_path)
        rows = conn.execute("SELECT title, content FROM posts ORDER BY id").fetchall()
        conn.close()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("기사 A", "기존 본문"))
        self.assertEqual(rows[1], ("기사 C", "요약 C"))

    @patch("seed.fetch_news_items")
    def test_seed_news_uses_empty_content_when_summary_missing(self, mock_fetch_news_items):
        mock_fetch_news_items.return_value = [
            {
                "title": "기사 D",
                "summary": "",
                "link": "https://example.com/d",
                "published": "Sun, 26 Apr 2026 09:03:00 +0900",
            }
        ]

        seed.seed_news_posts(limit=10)

        conn = sqlite3.connect(self.db_path)
        row = conn.execute("SELECT title, content FROM posts LIMIT 1").fetchone()
        conn.close()

        self.assertEqual(row, ("기사 D", ""))

    @patch("seed.fetch_news_items")
    def test_main_prints_added_count_log(self, mock_fetch_news_items):
        mock_fetch_news_items.return_value = [
            {
                "title": "기사 E",
                "summary": "요약 E",
                "link": "https://example.com/e",
                "published": "Sun, 26 Apr 2026 09:04:00 +0900",
            }
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            seed.main()

        self.assertIn("1건 추가됨", output.getvalue())


if __name__ == "__main__":
    unittest.main()
