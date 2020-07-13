from flask import Flask, request, Blueprint, render_template, flash, redirect, url_for
import json
import profile_build

app = Flask(__name__)
app.register_blueprint(profile_build.bp)
from flask_login import UserMixin
from flask_wtf import Form
from wtforms import TextField, BooleanField, StringField, PasswordField, TextAreaField, SubmitField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, LoginManager
import os


app = Flask(__name__)
login = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/users"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User: {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('welcome/welcome.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return render_template('login.html', form=form)

        login_user(user, remember=form.remember_me.data)
        return render_template('welcome/welcome.html')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('welcome/welcome.html')
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

