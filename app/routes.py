from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, CommentForm, ConnectionRequestForm, PostForm
from app.models import User, Comment
from flask_login import current_user, login_user, logout_user, login_required
from app.api import bp, github_blueprint
from flask_dance.contrib.github import github
from app.api.users import user_get_lang
from flask import session, request
import collections



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/comments/delete")
@login_required
def delete_comment():
    if not current_user.is_authenticated:
        return redirect(url_for('github.login'))

    comment_id = request.args.get("comment_id", 0, type=int)

    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('user_feed'))


@app.route('/feed', methods=['GET', 'POST'])
@login_required
def user_feed():
    if not current_user.is_authenticated:
        return redirect(url_for('github.login'))

    form = CommentForm()

    if form.validate_on_submit():
        user_id = current_user.id
        comment = Comment(message=form.message.data, user_id=user_id)
        db.session.add(comment)
        db.session.commit()

    page = request.args.get('page', 1, type=int)
    comments = Comment.query.order_by(Comment.date_posted.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for('user_feed', page=comments.next_num) \
        if comments.has_next else None

    prev_url = url_for('user_feed', page=comments.prev_num) \
        if comments.has_prev else None

    return render_template('user_feed.html', form=form, comments=comments.items, next_url=next_url,
                           prev_url=prev_url, current_user_id = current_user.id )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('github.login'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data):
            return redirect(url_for('github.login'))

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
        return redirect(url_for('home'))

    return render_template('login.html', title='Sign In', form=form)


app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/github', methods=['GET', 'POST'])
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        return redirect(url_for('home'))

    return '<h1>Request failed!</h1>'


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    current = User.query.get(current_user.id)
    current.authentication = True
    db.session.commit()
    account_info = github.get('/user')
    account_info_json = account_info.json()

    if current.languages is None:
        account_languages = user_get_lang(account_info_json['login'], github.token['access_token'])
        current.languages = account_languages
        db.session.commit()

    if current.github is None:
        github_account = account_info_json['login']
        current.github = github_account
        db.session.commit()

    return redirect(url_for('profile'))


@app.route('/delete', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get_or_404(current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash("Your account was successfully deleted")
    return redirect(url_for('login'))


@app.route('/connections', methods=['GET', 'POST'])
@login_required
def connections():
    user_languages = current_user.languages
    lang_list = []

    ordered_lang = collections.OrderedDict(sorted(user_languages.items(), key=lambda x: x[1], reverse=True))

    for key in ordered_lang:
        lang_list.append(key)

    len_lang = len(lang_list)

    if len_lang == 0:
        people = User.query.filter(User.username != current_user.username).all()
    else:
        favorite_lang = lang_list[0]
        people = User.query.filter(User.username != current_user.username, User.languages.has_key(favorite_lang)).all()

    requests = current_user.get_requests()
    form = ConnectionRequestForm()
    return render_template('connections.html', form=form, usernames=people, requests=requests)


@app.route('/connections/send_request/<username>', methods=['POST'])
@login_required
def send_request(username):
    form = ConnectionRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        current_user.request(user)
        db.session.commit()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('profile'))
        current_user.request(user)
        db.session.commit()
        flash('connection request sent to {}!'.format(username))
        return redirect(url_for('connections', username=username))
    else:
        return redirect(url_for('profile'))

@app.route('/connections/accept_request/<username>', methods=['POST'])
@login_required
def accept_request(username):
    user = User.query.filter_by(username=username).first()
    current_user.accept_request(user)
    db.session.commit()
    flash('Connection request accepted!')
    return redirect(url_for('connections', username=username))


@app.route('/help')
def help_page():
    return render_template('help.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = PostForm()
    if form.validate_on_submit():
        post = Comment(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('profile'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.connected_posts().order_by(Comment.date_posted.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('profile', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('profile', page=posts.prev_num) \
        if posts.has_prev else None

    user_languages = current_user.languages
    lang_list = []

    ordered_lang = collections.OrderedDict(sorted(user_languages.items(), key=lambda x: x[1], reverse=True))

    for key in ordered_lang:
        lang_list.append(key)

    len_lang = len(lang_list)
    conn_page = request.args.get('conn_page', 1, type=int)

    if len_lang == 0:
        people = User.query.filter(User.username != current_user.username).paginate(conn_page, 5)
    else:
        favorite_lang = lang_list[0]
        people = User.query.filter(User.username != current_user.username, User.languages.has_key(favorite_lang)).paginate(conn_page,5)

    conn_form = ConnectionRequestForm()


    conn_next_url = url_for('profile', conn_page=people.next_num) \
        if people.has_next else None
    conn_prev_url = url_for('profile', conn_page=people.prev_num) \
        if people.has_prev else None

    return render_template('profile.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url, user=current_user, form_conn=conn_form,
                           post_conn=people.items, next_url_conn=conn_next_url,
                           prev_url_conn=conn_prev_url)
