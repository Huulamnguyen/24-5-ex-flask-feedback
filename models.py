from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


# todo: connect database
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


# TODO: MODEL USER
class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(60), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    # TODO: REGISTER METHOD, CREATE NEW USERNAME AND PASSWORD THEN STORE IT AT DATABASE
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # * turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # * return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    # TODO: AUTHENTICATE METHOD, WHEN USER INPUT PASSWORD FROM FORM AND COMPARE IT TO DATABASE
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
            Return user if valid; else return False.
        """
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            # * return user instance
            return u
        else:
            return False
