import json
import os
import sqlite3
import tempfile
import unittest

from init_db import init_db


class SeedSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "seed_test.db")
        self.seed_path = os.path.join(self.temp_dir.name, "seed.json")
        seed_rows = [
            {
                "title": "시드 제목 1",
                "content": "시드 본문 1",
                "image": None,
                "created_at": "2026-04-01 10:00:00",
            },
            {
                "title": "시드 제목 2",
                "content": "시드 본문 2",
                "image": None,
                "created_at": "2026-04-02 10:00:00",
            },
        ]
        with open(self.seed_path, "w", encoding="utf-8") as f:
            json.dump(seed_rows, f, ensure_ascii=False)

        os.environ["DB_PATH"] = self.db_path
        os.environ["POSTS_SEED_PATH"] = self.seed_path

    def tearDown(self):
        os.environ.pop("DB_PATH", None)
        os.environ.pop("POSTS_SEED_PATH", None)
        self.temp_dir.cleanup()

    def test_init_db_imports_seed_when_table_is_empty(self):
        init_db()
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        first = conn.execute("SELECT title FROM posts ORDER BY id LIMIT 1").fetchone()
        conn.close()

        self.assertEqual(count, 2)
        self.assertIsNotNone(first)
        self.assertEqual(first[0], "시드 제목 1")

    def test_init_db_does_not_duplicate_seed_on_second_run(self):
        init_db()
        init_db()
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        conn.close()

        self.assertEqual(count, 2)

    def test_init_db_uses_default_seed_path_when_env_missing(self):
        os.environ.pop("POSTS_SEED_PATH", None)
        default_seed_path = os.path.join(os.getcwd(), "seed", "local_posts_seed.json")
        with open(default_seed_path, "r", encoding="utf-8") as f:
            local_seed = json.load(f)

        init_db()
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        conn.close()

        self.assertEqual(count, len(local_seed))


if __name__ == "__main__":
    unittest.main()
