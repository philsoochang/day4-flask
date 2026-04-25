import os
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    db = sqlite3.connect("board.db")
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()


def save_image(file):
    if file and file.filename and allowed_file(file.filename):
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return filename
    return None


@app.route("/")
def post_list():
    db = get_db()
    posts = db.execute(
        "SELECT id, title, content, image, created_at FROM posts ORDER BY created_at DESC"
    ).fetchall()
    db.close()
    return render_template("list.html", posts=posts)


@app.route("/write", methods=["GET", "POST"])
def write_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image = save_image(request.files.get("image"))
        db = get_db()
        db.execute("INSERT INTO posts (title, content, image) VALUES (?, ?, ?)", (title, content, image))
        db.commit()
        db.close()
        return redirect(url_for("post_list"))
    return render_template("write.html")


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    db = get_db()
    post = db.execute(
        "SELECT id, title, content, image, created_at FROM posts WHERE id = ?", (post_id,)
    ).fetchone()
    db.close()
    return render_template("detail.html", post=post)


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    db = get_db()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image = save_image(request.files.get("image"))
        if image is None:
            row = db.execute("SELECT image FROM posts WHERE id = ?", (post_id,)).fetchone()
            image = row["image"] if row else None
        db.execute("UPDATE posts SET title = ?, content = ?, image = ? WHERE id = ?", (title, content, image, post_id))
        db.commit()
        db.close()
        return redirect(url_for("post_detail", post_id=post_id))
    post = db.execute(
        "SELECT id, title, content, image, created_at FROM posts WHERE id = ?", (post_id,)
    ).fetchone()
    db.close()
    return render_template("write.html", post=post)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
