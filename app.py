from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, EditUserForm, FeedbackForm
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
        return redirect(f'/users/{new_user.username}')
    return render_template("register.html", form=form)


# TODO: LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login_user():
    if "user_name" in session:
        return redirect(f"/users/{session['user_name']}")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session["user_name"] = user.username
            return redirect(f"/users/{user.username}")
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


# TODO: User/usernames route
@app.route("/users/<username>", methods=["GET", "POST"])
def show_user(username):
    """ Show logged-in-user information"""

    # todo: If user is not in session, it will redirect to root route
    if "user_name" not in session or username != session['user_name']:
        flash("Please login first!", "danger")
        return redirect("/")

    # todo: get user's info
    user = User.query.get_or_404(username)
    form = EditUserForm(obj=user)

    feedbacks = Feedback.query.all()
    return render_template("user.html", user=user, form=form, feedbacks=feedbacks)


# TODO: Delete Route
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete user info"""
    if "user_name" not in session or username != session['user_name']:
        flash("Please login first!", "danger")
        return redirect("/")

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("user_name")

    return redirect("/")


# TODO: New Feedback Route
@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if "user_name" not in session or username != session['user_name']:
        flash("Please login first!", "danger")
        return redirect("/")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()
        flash("Sucessfully Added New Feedback", "success")
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback.html", form=form)


# TODO: Update existing feedback
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "user_name" not in session or feedback.username != session['user_name']:
        flash("Please login first!", "danger")
        return redirect("/")

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("edit_feedback.html", form=form, feedback=feedback)


# TODO: Delete feedback
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """ Delete feedback"""
    feedback = Feedback.query.get(feedback_id)

    if "user_name" not in session or feedback.username != session['user_name']:
        flash("Please login first!", "danger")
        return redirect("/")

    db.session.delete(feedback)
    db.session.commit()
    flash("Your feedback has been deleted", "info")

    return redirect(f"/users/{feedback.username}")
