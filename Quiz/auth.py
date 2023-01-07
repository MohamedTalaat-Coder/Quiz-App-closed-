import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from Quiz.db import connect_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = connect_db()
        cursor = db.cursor()

        error = None

        if not username:
            error = "username is required"
        elif not password:
            error = "password is required"
        
        print("-------------->", error, username, password)
        
        cursor.execute(f"INSERT INTO user (username, password) VALUES ('{username}', '{generate_password_hash(password)}')")
        db.commit()
    return render_template("auth/register.html")

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        cursor = db.cursor()
        error = None
        cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
        user = cursor.fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user[2], password):
            error = "incorrect password"

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():

    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM user WHERE id = '{user_id}' ")
        g.user = cursor.fetchone()
        print("userid", g.user, "session", user_id)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
