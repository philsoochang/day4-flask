import json
import os
import sqlite3


def seed_posts_if_empty(db):
    seed_path = os.environ.get("POSTS_SEED_PATH", "")
    if not seed_path or not os.path.exists(seed_path):
        return

    existing_count = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    if existing_count > 0:
        return

    with open(seed_path, "r", encoding="utf-8") as f:
        seed_posts = json.load(f)

    rows = []
    for post in seed_posts:
        rows.append(
            (
                post.get("title", ""),
                post.get("content", ""),
                post.get("image"),
                post.get("created_at"),
            )
        )

    db.executemany(
        "INSERT INTO posts (title, content, image, created_at) VALUES (?, ?, ?, ?)",
        rows,
    )


def init_db():
    db_path = os.environ.get("DB_PATH", "board.db")
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    db = sqlite3.connect(db_path)
    db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    seed_posts_if_empty(db)
    db.commit()
    db.close()


if __name__ == "__main__":
    init_db()
