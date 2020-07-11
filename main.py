from flask import Flask, request, Blueprint, render_template
import json
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/users"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.DataRequired()])

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique = True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if request:
            uname = request.form.getlist('username')[0]
            pword = request.form.getlist('password')[0]
            new_user = UserModel(username=uname, password=pword)
            try:
                db.session.add(new_user)
                db.session.commit()
            except exc.IntegrityError:
                 db.session.rollback()
                 return render_template('duplicate_error.html', form=form)
            return {"message": f"User {new_user.username} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

        flash('Welcome back')
    return render_template('login.html', form=form)



@app.route('/')
def home():
    return render_template('welcome/welcome.html')

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
