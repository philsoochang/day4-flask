import os
import re
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify
from markupsafe import Markup

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "uploads")
ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp", "bmp", "svg",
    "ico", "tiff", "tif", "avif",
}


@app.template_filter("render_content")
def render_content(text):
    if not text:
        return ""
    def img_repl(m):
        alt = m.group(1) or ""
        url = m.group(2)
        return (
            f'<img src="{url}" alt="{alt}" '
            f'class="w-full rounded-lg my-stack-md" loading="lazy"/>'
        )
    html = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img_repl, str(text))
    return Markup(html)


@app.template_filter("strip_images")
def strip_images(text):
    if not text:
        return ""
    return re.sub(r"!\[[^\]]*\]\([^)]+\)", "", str(text))


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    db_path = os.environ.get("DB_PATH", "board.db")
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db


def save_image(file):
    if file and file.filename and allowed_file(file.filename):
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return filename
    return None


@app.route("/upload-image", methods=["POST"])
def upload_image():
    file = request.files.get("image")
    if not file or not file.filename or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400
    filename = save_image(file)
    url = url_for("static", filename=f"uploads/{filename}", _external=True)
    return jsonify({"url": url})


@app.route("/")
def post_list():
    per_page = 10
    query = request.args.get("q", "").strip()
    sort = request.args.get("sort", "latest").strip()
    sort_map = {
        "latest": "created_at DESC",
        "oldest": "created_at ASC",
        "title_asc": "title COLLATE NOCASE ASC",
    }
    sort = sort if sort in sort_map else "latest"
    order_by = sort_map[sort]

    try:
        page = int(request.args.get("page", 1))
    except (TypeError, ValueError):
        page = 1
    page = max(page, 1)

    db = get_db()
    if query:
        keyword = f"%{query}%"
        total_posts = db.execute(
            "SELECT COUNT(*) FROM posts WHERE title LIKE ? OR content LIKE ?",
            (keyword, keyword),
        ).fetchone()[0]
    else:
        total_posts = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]

    total_pages = max(1, (total_posts + per_page - 1) // per_page)
    page = min(page, total_pages)
    offset = (page - 1) * per_page

    if query:
        posts = db.execute(
            f"SELECT id, title, content, image, created_at FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY {order_by} LIMIT ? OFFSET ?",
            (keyword, keyword, per_page, offset),
        ).fetchall()
    else:
        posts = db.execute(
            f"SELECT id, title, content, image, created_at FROM posts ORDER BY {order_by} LIMIT ? OFFSET ?",
            (per_page, offset),
        ).fetchall()
    db.close()

    return render_template(
        "list.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        has_prev=page > 1,
        has_next=page < total_pages,
        query=query,
        sort=sort,
        is_search=bool(query),
        total_posts=total_posts,
    )


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


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    db = get_db()
    post = db.execute("SELECT image FROM posts WHERE id = ?", (post_id,)).fetchone()
    if post and post["image"]:
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], post["image"])
        if os.path.exists(img_path):
            os.remove(img_path)
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    db.close()
    return redirect(url_for("post_list"))


with app.app_context():
    from init_db import init_db
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
