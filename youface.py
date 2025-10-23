# youface.py
import time
import flask
import timeago
import tinydb

from handlers import friends, login, posts

app = flask.Flask(
    __name__,
    template_folder='webpage',     
    static_folder='webpage',       
    static_url_path=''             
)

@app.template_filter('convert_time')
def convert_time(ts):
    return timeago.format(ts, time.time())

# blueprints
app.register_blueprint(friends.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(posts.blueprint)

app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)
