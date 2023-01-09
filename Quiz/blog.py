from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import os
from Quiz.auth import login_required
from werkzeug.exceptions import abort
from Quiz.db import connect_db

def get_question(id, check_user=True):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT q.id, Question, Answer, user_id FROM questions q JOIN user u ON q.user_id = u.id WHERE q.id = {id}")
    question = cursor.fetchone()

    if question is None:
        abort(404, f"Question id {id} doesn't exist.")
    if check_user and question[3] != g.user[0]:
        abort(403)
    
    return question



bp = Blueprint("blog", __name__)

@bp.route("/hello")
def hello():
    return "hello, world"


@bp.route("/")
def index():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT id, Question, Answer FROM questions WHERE user_id = {g.user[0]}  ORDER BY id DESC ")
    questions = cursor.fetchall()
    return render_template("blog/index.html", questions=questions)

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

@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    question = get_question(id)
    if request.method == "POST":
        question = request.form['question']
        answer = request.form['answer']
        error = None
        if not question:
            error = "Question is required"
        if error is not None:
            flash(error)

        else:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(f"UPDATE questions SET Question = '{question}', Answer = '{answer}' WHERE id = {id}")
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template("blog/update.html", question=question)

@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(id):
    question = get_question(id)
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM questions WHERE id = {id}")
    db.commit()
    return redirect(url_for("blog.index"))