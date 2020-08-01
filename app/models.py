from sqlalchemy import UniqueConstraint

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta
from hashlib import md5
from datetime import datetime
from sqlalchemy.dialects.postgresql.json import JSONB



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000), index=False, unique=False)
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
        return '<Post {}>'.format(self.body)

    # def __init__(self, body, user_id):
    #     self.body = body
    #     self.user_id = user_id
    #     self.date_posted = datetime.utcnow()


connections = db.Table('connections',
                       db.Column('sender_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('recipient_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('are_connected', db.Boolean, default=False)
                       )


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    authentication = db.Column(db.Boolean, default=False)
    posts = db.relationship('Comment', backref='author', lazy='dynamic')
    languages = db.Column(JSONB, default=None)
    connected = db.relationship(
        'User', secondary=connections,
        primaryjoin=(connections.c.sender_id == id),
        secondaryjoin=(connections.c.recipient_id == id),
        backref=db.backref('connections', lazy='dynamic'), lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User: {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def request(self, users):
        if not self.is_requested(users):
            self.connected.append(users)

    def is_requested(self, users):
        return self.connected.filter(
            connections.c.recipient_id == users.id).count() > 0

    def get_requests(self):
        requests = User.query.join(connections, (
                connections.c.recipient_id == self.id)).filter(
                connections.c.sender_id == User.id)
        return requests

    def is_connected(self, users):
        return self.connected.filter(
            connections.c.recipient_id == users.id).filter(connections.c.are_connected == "true").count() > 0.

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def connected_posts(self):
        connected = Comment.query.join(
            connections, (connections.c.recipient_id == Comment.user_id)).filter(
            connections.c.sender_id == self.id)
        own = Comment.query.filter_by(user_id=self.id)
        return connected.union(own).order_by(Comment.date_posted.desc())


