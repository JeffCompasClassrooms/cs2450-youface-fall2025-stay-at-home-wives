import flask
import tinydb

from handlers import copy
from db import users, helpers

blueprint = flask.Blueprint("login", __name__)

@blueprint.route('/loginscreen')
def loginscreen():
    """serves the login page if not logged in, otherwise displays warning and goes to index"""
    db = helpers.load_db()

    # allow ?force=1 to always show the page
    force = flask.request.args.get('force')

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if not force and username and password:
        if users.get_user(db, username, password):
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title, subtitle=copy.subtitle)

@blueprint.route('/login', methods=['POST'])
def login():
    """Create, delete, or log in a user based on button clicked, staying on page for 
    failed login, account creation, or account deletion and doing to index otherwise"""
    db = helpers.load_db()

    username = flask.request.form.get('username', '').strip()
    password = flask.request.form.get('password', '').strip()
    submit   = flask.request.form.get('type')

    # Helper to make a response that sets/clears cookies
    def set_cookies_and_redirect(u=None, p=None, dest='login.index'):
        resp = flask.make_response(flask.redirect(flask.url_for(dest)))
        if u is None or p is None:
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
        else:
            resp.set_cookie('username', u)
            resp.set_cookie('password', p)
        return resp

    if submit == 'Create':
        if users.new_user(db, username, password) is None:
            flask.flash(f'Username {username} already taken!', 'danger')
            return set_cookies_and_redirect(None, None, 'login.loginscreen')
        flask.flash(f'User {username} created successfully!', 'success')
        return set_cookies_and_redirect(username, password, 'login.index')

    elif submit == 'Delete':
        if users.delete_user(db, username, password):
            flask.flash(f'User {username} deleted successfully!', 'warning')
            return set_cookies_and_redirect(None, None, 'login.loginscreen')
        else:
            flask.flash('User not found or wrong password.', 'danger')
            return set_cookies_and_redirect(None, None, 'login.loginscreen')

    else:  # 'Login'
        user = users.get_user(db, username, password)
        if not user:
            flask.flash('Invalid credentials. Please try again.', 'danger')
            return set_cookies_and_redirect(None, None, 'login.loginscreen')

        flask.flash(f'Welcome back, {username}!', 'success')
        return set_cookies_and_redirect(username, password, 'login.index')

@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user by removing cookies, serves login page."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/')
def index():
    """Serves the home page for the user."""
    db = helpers.load_db()

    # Who (if anyone) is logged in?
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users.get_user(db, username, password) if username and password else None
    logged_in = bool(user)

    # Gather crews (show everything to guests too) [change to crews]
    crews_table = db.table('crews')
    docs = []
    for doc in crews_table:
        docs.append(doc)
    docs.sort(key=lambda d: d['time'], reverse=True)

    friends_list = users.get_user_friends(db, user) if logged_in else []

    return flask.render_template(
        'index.html',
        title=copy.title,
        subtitle=copy.subtitle,
        user=user,
        username=username,
        friends=friends_list,
        crews=docs,
        logged_in=logged_in,
    )

@blueprint.route('/template')
def template_page():
    return flask.render_template('template.html')
