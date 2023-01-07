from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import os
from Quiz.auth import login_required
from werkzeug.exceptions import abort
from Quiz.db import connect_db

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT id, Question, Answer FROM questions WHERE user_id = {g.user[0]}  ORDER BY id DESC ")
    questions = cursor.fetchall()

    return render_template("blog/index.html", posts=questions)

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        question = request.form['question']
        question = question.replace("'", "''")
        answer = request.form['answer']
        error = None
        if not question:
            error = "Question required"
        if error is not None:
            flash(error)
        else:
            db = connect_db()
            cuursor = db.cursor()
            cuursor.execute(f"INSERT INTO questions (Question, Answer, user_id) VALUES ('{question}', '{answer}', {g.user[0]})")
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")