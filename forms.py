from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


# TODO: USER FORM
class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(
        min=0, max=20, message="Maximum 20 characters")])

    password = PasswordField("Password", validators=[InputRequired()])

    email = StringField("Email", validators=[
                        InputRequired(), Email(message="Invalid email address"), Length(min=0, max=50, message="Maximum 50 characters")])

    first_name = StringField("First Name", validators=[InputRequired(), Length(
        min=0, max=50, message="Maximum 50 characters")])

    last_name = StringField("Last Name", validators=[InputRequired(), Length(
        min=0, max=50, message="Maximum 50 characters")])


# TODO: LOGIN FORM
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(
        min=0, max=20, message="Maximum 20 characters")])

    password = PasswordField("Password", validators=[InputRequired()])
