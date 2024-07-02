from flask import Blueprint, render_template, request, flash, redirect, session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_required

db = SQL("sqlite:///users.db")

auth = Blueprint('auth', __name__)

@auth.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@auth.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        if not username:
            flash('Please enter a username', category='error')

        elif not password:
            flash('Please enter a password', category='error') 

        elif len(rows) != 1 or not check_password_hash(
            rows[0]["password"], password
        ):
            flash('Invalid username and/or password', category='error')
        else:
            session["user_id"] = rows[0]["id"]
            flash('Logged in succesfully!', category='success')
            return redirect("/")
    return render_template("login.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect("/login")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')
        confirmation = request.form.get('password2')

        r = db.execute(
            "SELECT * FROM users WHERE username = ?", username
            )

        if not username:
            flash('Please enter a username', category='error')
        elif len(r) != 0:
            flash('Username already exists', category='error')
        elif not password:
            flash('Please enter a password', category='error')
        elif password != confirmation:
            flash('Passwords do not match', category='error')
        else:
            pass_hash = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", username, pass_hash
            )
            id = db.execute(
                "SELECT * FROM users WHERE username = ?", username
                )
            session["user_id"] = id[0]["id"]
            flash('Account created!')
            return redirect("/")
    return render_template("signup.html", category='success')