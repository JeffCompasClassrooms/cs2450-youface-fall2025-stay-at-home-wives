# youface.py
import time
import flask
import timeago
import tinydb
from db import helpers as helpers_db, users as users_db
from flask import request
from handlers import friends, login, posts

app = flask.Flask(
    __name__,
    template_folder='frontend',     
    static_folder='frontend',       
    static_url_path=''             
)

@app.template_filter('convert_time')
def convert_time(ts):
    return timeago.format(ts, time.time())

@app.context_processor
def inject_auth():
    db = helpers_db.load_db()
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    user = users_db.get_user(db, username, password) if username and password else None
    return {
        'username': username,
        'user': user,
        'logged_in': bool(user),
    }

# blueprints
app.register_blueprint(friends.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(posts.blueprint)

app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)
