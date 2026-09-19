import os
import sqlite3

from flask import Flask, flash, g, redirect, render_template, request, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.path.join(app.instance_path, "dashboard.sqlite3"),
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        get_db().execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        get_db().commit()

    @app.route("/", methods=("GET", "POST"))
    def index():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()

            if not title or not content:
                flash("제목과 내용을 모두 입력해 주세요.", "error")
            elif len(title) > 120:
                flash("제목은 120자 이하로 입력해 주세요.", "error")
            else:
                db = get_db()
                db.execute(
                    "INSERT INTO posts (title, content) VALUES (?, ?)",
                    (title, content),
                )
                db.commit()
                flash("게시물이 등록되었습니다.", "success")
                return redirect(url_for("index"))

        posts = get_db().execute(
            "SELECT id, title, content, created_at FROM posts ORDER BY id DESC"
        ).fetchall()
        return render_template("index.html", posts=posts)

    with app.app_context():
        init_db()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
