from flask import Flask, request, render_template
from wtforms import Form, BooleanField, StringField, PasswordField, validators
# Previous imports remain...
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/users"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

class UserModel(db.Model):
    __tablename__ = 'users'

    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"






@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['uname']
#     processed_text = text.upper()
#     return processed_text


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = UserModel(form.username.data, form.password.data)
        # return request
        # print(request.form.getlist('username'))
        # uname = request.form.getlist('username')
        # print(uname[0])

        # print('Hello world!', file=sys.stderr)
        if request:
            uname = request.form.getlist('username')[0]
            pword = request.form.getlist('password')[0]
            # data = request.form.getlist
            new_user = UserModel(username=uname, password=pword)
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"User {new_user.username} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

        # db_session.add(user)
        flash('Welcome back')
        return redirect(url_for('/'))
    return render_template('login.html', form=form)
#
# @app.route('/cars', methods=['POST', 'GET'])
# def handle_cars():
#     if request.method == 'POST':
#         if request.is_json:
#             data = request.get_json()
#             new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'])
#             db.session.add(new_car)
#             db.session.commit()
#             return {"message": f"car {new_car.name} has been created successfully."}
#         else:
#             return {"error": "The request payload is not in JSON format"}
#
#     elif request.method == 'GET':
#         cars = CarsModel.query.all()
#         results = [
#             {
#                 "name": car.name,
#                 "model": car.model,
#                 "doors": car.doors
#             } for car in cars]
#
#         return {"count": len(results), "cars": results}

    # form = RegistrationForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     user = User(form.username.data, form.email.data,
    #                 form.password.data)
    #     db_session.add(user)
    #     flash('Thanks for registering')
    #     return redirect(url_for('login'))
    # return render_template('register.html', form=form)
