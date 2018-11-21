# main backend entry point

import os
from flask import Flask, jsonify, request, session, send_file, flash, render_template, redirect
from flask_session import Session
from models import *
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# page routes config


@app.route("/")
@login_required
def index():
    # main app
    return send_file("templates/index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # login page handling

    # forget current user
    session.clear()

    # a post request
    if request.method == 'POST':
        # Ensure form was filled
        if not request.form.get('username'):
            flash("No username found!")
            return render_template("login.html")
        elif not request.form.get('password'):
            flash("No password found!")
            return render_template("login.html")

        # query db for user
        user = Profile.query.filter_by(
            username=request.form.get('username')).first()

        # check username exists & password match
        if user is None or not check_password_hash(user.password, request.form.get('password')):
            flash("Invalid username/password!")
            return render_template("login.html")

        # remember id
        session['user_id'] = user.id

        return redirect("/")

    else:
        # get request
        return render_template("login.html")


@app.route("/logout")
def logout():
    # log user out

    # clear session var
    session.clear()

    return redirect("/login")


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True, use_reloader=True)
