import flask
from db import posts as posts_db, helpers as helpers_db, users as users_db

blueprint = flask.Blueprint("posts", __name__)

@blueprint.route('/post', methods=['POST'])
def post():
    """Creates a new post."""
    db = helpers_db.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    text = flask.request.form.get('post', '').strip()
    if not text:
        flask.flash('Post cannot be empty.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    posts_db.add_post(db, user, text)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.get('/posts/<int:post_id>')
def view_post(post_id):
    """Show a single post with comments."""
    db = helpers_db.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password) if username and password else None

    p = posts_db.get_post_by_id(db, post_id)
    if not p:
        return ("Post not found", 404)

    posts_db.increment_views(db, post_id)
    return flask.render_template('posts.html', post=p, username=username, user=user)

@blueprint.post('/posts/<int:post_id>/comment')
def add_comment(post_id):
    """Add a comment to a post."""
    db = helpers_db.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to comment.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    body = flask.request.form.get('body', '').strip()
    if not body:
        flask.flash('Comment cannot be empty.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))

    ok = posts_db.add_comment(db, post_id, user['username'], body)
    if not ok:
        return ("Post not found", 404)

    return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))

@blueprint.get('/posts/new')
def new_post_form():
    db = helpers_db.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('Please log in to create a post.', 'warning')
        return flask.redirect(flask.url_for('login.loginscreen'))
    return flask.render_template('new_post.html', logged_in=True, user=user, username=username)

@blueprint.post('/posts/<int:post_id>/delete')

def delete_post(post_id):
    """Delete a post (only by its author)."""
    db = helpers_db.load_db()

    # must be logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to delete posts.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # must exist and belong to current user
    p = posts_db.get_post_by_id(db, post_id)
    if not p:
        flask.flash('Post not found.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    if p['user'] != user['username']:
        flask.flash('You can only delete your own posts.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))

    # delete
    posts_db.delete_post(db, post_id)
    flask.flash('Post deleted.', 'success')
    return flask.redirect(flask.url_for('login.index'))

@blueprint.post('/posts/<int:post_id>/comments/<int:idx>/delete')
def delete_comment(post_id, idx):
    """Allow a commenter (or the post owner) to delete a comment."""
    db = helpers_db.load_db()

    # must be logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to delete comments.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    p = posts_db.get_post_by_id(db, post_id)
    if not p:
        flask.flash('Post not found.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    comments = p.get('comments', [])
    if not (0 <= idx < len(comments)):
        flask.flash('Comment not found.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))

    comment = comments[idx]

    # permission: comment author OR post author
    if user['username'] not in (comment['author'], p['user']):
        flask.flash('You can only delete your own comment.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))

    if posts_db.delete_comment(db, post_id, idx):
        flask.flash('Comment deleted.', 'success')
    else:
        flask.flash('Could not delete comment.', 'danger')

    return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))
