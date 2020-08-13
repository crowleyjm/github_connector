from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, StringField, PasswordField, TextAreaField, SubmitField, validators, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=32)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    remember_me = BooleanField()

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class CommentForm(FlaskForm):
    message = StringField('message', validators=[DataRequired()])


class PostForm(FlaskForm):
    post = TextAreaField('Say something: ', validators=[DataRequired()])
    submit = SubmitField('Post')


class ConnectionRequestForm(FlaskForm):
    submit = SubmitField('Send Request')


class ConnectionRemoveForm(FlaskForm):
    submit = SubmitField('Remove Connection')

class SearchForm(FlaskForm):
    submit = SubmitField('search', validators=[DataRequired()])