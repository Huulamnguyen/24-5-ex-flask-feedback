from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_user_ex"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "flask_feedback_ex"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """ Redirect to register """
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """ Show regiser form and handle submit the form """
    form = UserForm()
    if form.validate_on_submit():
        # todo: get username, password, email, first_name, last_name from the register form
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # todo: add new user to users database
        new_user = User.register(
            username, password, email, first_name, last_name)
        db.session.add(new_user)

        # todo: because username is unique, it wil raise errors.
        # todo: this try to catch error and redirect to register form.
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken.  Please pick another")
            return render_template("register.html", form=form)

        # todo: create session to remember when user login
        session["user_name"] = new_user.username
        flash("Welcome! Successfully Created Your Account!", "success")
        return redirect('/secret')

    return render_template("register.html", form=form)


# TODO: LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login_user():

    if "user_name" in session:
        return redirect('/secret')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session["user_name"] = user.username
            return redirect("/secret")
        else:
            # todo: display errors if apply
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


# TODO: LOG OUT ROUTE
@app.route("/logout")
def logout_user():
    """ Log out Route """
    # todo: remove session
    session.pop("user_name")
    flash("Goodbye!", "info")
    return redirect("/")


# TODO: SECRET ROUTE
@app.route("/secret", methods=["GET", "POST"])
def show_secret():
    if "user_name" not in session:
        flash("Please login first!", "danger")
        return redirect("/")

    return render_template("secret.html")
