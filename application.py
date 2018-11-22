# main backend entry point

import os
from flask import Flask, jsonify, request, session, send_file, flash, render_template, redirect
from flask_session import Session
from models import *
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, get_dict, get_dict_array

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


@app.route("/register", methods=["GET", "POST"])
def register():
    # sign up user

    # clear any user
    session.clear()

    # post request
    if request.method == 'POST':

        # grab form info into vars
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # ensure params are passed
        if not first_name:
            flash("No first name found!")
            return render_template("register.html")
        elif not last_name:
            flash("No last name found!")
            return render_template("register.html")
        elif not email:
            flash("No email found!")
            return render_template("register.html")
        elif not username:
            flash("No username found!")
            return render_template("register.html")
        elif not password or not confirmation:
            # Ensure password was submitted
            flash("No password/confirmation found!")
            return render_template("register.html")
        elif password != confirmation:
            flash("Passwords don't match!")
            return render_template("register.html")

        # query db for profile with same username
        user = Profile.query.filter_by(username=username).first()

        # profile with username already exists
        if user:
            flash("Username already exists!")
            return render_template("register.html")

        # query db for profile with same email
        user = Profile.query.filter_by(email=email).first()

        # profile with email already exists
        if user:
            flash("Email already used!")
            return render_template("register.html")

        # make new user in db
        new = Profile(first_name, last_name, email, username,
                      generate_password_hash(password))
        db.session.add(new)
        db.session.commit()

        # save user login
        session['user_id'] = new.id

        return redirect("/")

    else:
        # send register page
        return render_template("register.html")

# api routes


@app.route("/api/profile", methods=["GET", "UPDATE", "DELETE"])
def profile_route():
    """
        GET:    req: profile_id?
                res: profile

        UPDATE: req:    profile_id?, first_name?, last_name?, mobile_no?,
                        email?, username?, password?
                res:    success, profile

        DELETE: req:    [null]
                res:    success
    """
    if request.method == "DELETE":
        # delete the current user

        if session.get('user_id') is None:
            return jsonify({"success": False, "message": "Profile not logged in!"})

        # grab user obj and delete
        profile = Profile.query.get(session.get('user_id'))
        db.session.delete(profile)
        db.session.commit()

        # clear the session
        session.clear()

        return jsonify({"success": True})

    elif request.method == "UPDATE":
        # update user info
        pass
    else:
        # send back user info if logged in
        # else send limited info for given profile id
        body = request.get_json()

        if not body:
            # send current user if logged in
            if session.get('user_id') is None:
                return jsonify({"success": False, "message": "Profile not logged in!"})

            # grab profile from db
            profile = Profile.query.get(session.get('user_id'))

            return jsonify({"success": True, "profile": get_dict(profile)})

        elif 'profile_id' in body:
            # profile of profile id
            profile = Profile.query.get(body['profile_id'])

            if not profile:
                return jsonify({"success": False, "message": "Profile with id not found!"})

            # TODO: only return non-sensitive info
            return jsonify({"success": True, "profile": get_dict(profile)})

        # should not happen
        return jsonify({"success": False, "message": "Invalid request!"})


@app.route("/api/page", methods=["GET", "POST"])
def page_route():
    """
        GET:    req: page_id
                res: page

        POST:   req: name!, desc!, category?
                res: success
    """

    if request.method == "POST":
        # can only do this if logged in
        # and logged in user will be admin & member
        if session.get('user_id') is None:
            return jsonify({"success": False, "message": "Not logged in!"})

        # grab req body
        body = request.get_json()

        # body validation
        if not body:
            return jsonify({"success": False, "message": "No request body!"})
        if 'name' not in body:
            return jsonify({"success": False, "message": "Page name not specified!"})
        if 'desc' not in body:
            return jsonify({"success": False, "message": "Page description not specified!"})

        # check if category provided
        category = ''
        if 'category' in body:
            category = body['category']

        # check if same nage page exists
        page = Page.query.filter_by(name=body['name']).first()
        if page:
            return jsonify({"success": False, "message": "Page with name already exists!"})

        # create page in db
        new = Page(body['name'], body['desc'], category)
        db.session.add(new)

        # grab profile to make him admin & member
        profile = Profile.query.get(session.get('user_id'))
        page.admins.append(profile)
        page.members.append(profile)

        # commit to db
        db.session.commit()

        return jsonify({"success": True})

    else:
        # if page_id exists return the page object
        body = request.get_json()

        # body validation
        if not body:
            return jsonify({"success": False, "message": "No request body!"})
        if 'page_id' not in body:
            return jsonify({"success": False, "message": "Page id not specified!"})

        # get page from db
        page = Page.query.get(body['page_id'])

        if not page:
            return jsonify({"success": False, "message": "Page with page_id doesn't exist!"})

        # increment views
        page.views += 1
        db.session.commit()

        return jsonify({"success": True, "page": get_dict(page)})


@app.route("/api/post", methods=["GET", "POST"])
def post_route():
    """
        GET:    req: user_id?, page_id?
                res: [posts]

        POST:   req: type!, body!, page_id?
                res: success
    """

    if request.method == "POST":
        # can only do this if logged in for profile
        # or page if profile is admin

        if session.get('user_id') is None:
            return jsonify({"success": False, "message": "Profile not logged in!"})

        # grab req body
        body = request.get_json()

        if not body:
            return jsonify({"success": False, "message": "No request body!"})
        if 'type' not in body:
            return jsonify({"success": False, "message": "Post type not specified!"})
        if 'body' not in body:
            return jsonify({"success": False, "message": "Post body not specified!"})

        # if body has page_id make post from page else make profile post
        if 'page_id' in body:

            # check if page exists
            page = Page.query.get(body['page_id'])
            if not page:
                return jsonify({"success": False, "message": "Page doesn't exist"})

            # TODO: check if user is admin of page

            # add post to db
            post = Post(body['type'], body['body'],
                        None, body['page_id'])
            db.session.add(post)
        else:
            # make current user post
            post = Post(body['type'], body['body'],
                        session.get('user_id'), None)
            db.session.add(post)

        db.session.commit()

        return jsonify({"success": True})

    else:
        # if user_id or page_id exists return posts for that
        # else return posts of current logged in user
        body = request.get_json()

        if not body:
            # return current logged in profile posts

            if session.get('user_id') is None:
                return jsonify({"success": False, "message": "Profile not logged in!"})

            # grab profile
            profile = Profile.query.get(session.get('user_id'))

            return jsonify({"success": True, "posts": get_dict_array(profile.posts)})

        elif 'user_id' in body:
            # return posts for given userid

            # grab profile
            profile = Profile.query.get(body['user_id'])

            return jsonify({"success": True, "posts": get_dict_array(profile.posts)})

        elif 'page_id' in body:
            # return posts from page

            # grab page
            page = Page.query.get(body['page_id'])

            return jsonify({"success": True, "posts": get_dict_array(page.posts)})

        # should not happen
        return jsonify({"success": False, "message": "Invalid request!"})


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True, use_reloader=True)