from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta
import base64
from datetime import datetime



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000), index=False, unique=False)
    date_posted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)

    def get_user(self):
        return User.query.get(
            self.user_id
        )

    def get_date_posted(self):
        if self.date_posted:
            return self.date_posted.strftime("%b %d %Y %H:%M:%S")
        else:
            return ''

    def __repr__(self):
        return self.message

    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id
        self.date_posted = datetime.utcnow()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    authentication = db.Column(db.Boolean, default=False)
    languages = db.Column(db.JSON, default=None)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User: {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
