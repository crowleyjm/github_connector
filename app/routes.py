from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from flask_dance.contrib.github import make_github_blueprint, github


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    

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
        login_user(user, remember=form.remember_me.data)
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data):
            return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('github.login'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('github.login'))

    return render_template('login.html', title='Sign In', form=form)


github_blueprint = make_github_blueprint(client_id='863e1284b52035734311',
                                         client_secret='9f23aa1f7ff8831063365c6e0d06b54e7bab9675')

app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/github', methods=['GET', 'POST'])
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        user = User.query.filter_by(username=current_user).first()
        user.authentication = True
        db.session.commit()
        return render_template('welcome.html')

    return '<h1>Request failed!</h1>'


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('welcome.html')
