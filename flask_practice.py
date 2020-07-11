from flask import Flask, request, render_template, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc


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
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.DataRequired()])

class UserModel(db.Model):
    __tablename__ = 'users'

    # id = db.Column(db.Integer, primary_key=True)
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

        # db_session.add(user)
        flash('Welcome back')
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return render_template('index.html')



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
