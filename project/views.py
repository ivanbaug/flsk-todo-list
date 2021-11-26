import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, render_template, request, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
from . import db
from .models import User, TDList, Task
from .forms import LoginForm, NewUserForm

INFO_EMAIL = os.environ.get("INFO_EMAIL")

# Authentication views

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # find user by email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("main.index"))
            else:
                flash("Wrong password or user, please try again.")
                return redirect(url_for("auth.login"))
        else:
            flash("Wrong user or password, please try again.")
            return redirect(url_for("auth.login"))

    return render_template("login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    nform = NewUserForm()

    if nform.validate_on_submit():
        # If user's email already exists
        if User.query.filter_by(email=nform.email.data).first():
            # Send flash messsage
            flash("You've already signed up with that email, log in instead!")
            # Redirect to /login route.
            return redirect(url_for("auth.login"))

        hash_and_salted_password = generate_password_hash(
            nform.password.data, method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(
            email=nform.email.data,
            name=nform.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()

        # Logging in right after registering so the user can access the
        # full page

        login_user(new_user)

        return redirect(url_for("main.index"))
    if request.method == "POST":
        # Send flash messsage
        flash("Error, check the submitted data, did you confirm your password?")
    return render_template("signup.html", form=nform)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# Main views

main = Blueprint("main", __name__)


@main.route("/")
def index():
    # cafes = Cafe.query.all()
    return render_template("index.html")
