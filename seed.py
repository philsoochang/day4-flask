import os
import sqlite3

from crawler import fetch_news_items


def ensure_posts_table(db):
    db.execute(
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


def seed_news_posts(limit=10):
    db_path = os.environ.get("DB_PATH", "board.db")
    db = sqlite3.connect(db_path)
    ensure_posts_table(db)

    existing_titles = {
        row[0]
        for row in db.execute("SELECT title FROM posts").fetchall()
    }

    news_items = fetch_news_items(limit=limit)
    rows_to_insert = []

    for item in news_items:
        title = (item.get("title") or "").strip()
        if not title or title in existing_titles:
            continue

        content = item.get("summary") or ""
        rows_to_insert.append((title, content, None))
        existing_titles.add(title)

    if rows_to_insert:
        db.executemany(
            "INSERT INTO posts (title, content, image) VALUES (?, ?, ?)",
            rows_to_insert,
        )

    db.commit()
    db.close()

    return len(rows_to_insert)


def main():
    added_count = seed_news_posts(limit=10)
    print(f"{added_count}건 추가됨")


if __name__ == "__main__":
    main()
