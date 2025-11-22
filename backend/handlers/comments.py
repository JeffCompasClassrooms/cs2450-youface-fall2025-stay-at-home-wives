import flask
from db import comments as comments_db, helpers as helpers_db, users as users_db
blueprint = flask.Blueprint("comments", __name__)

@blueprint.route('/comment/<int:parent>', methods=['POST'])
def post(parent):
    """Creates a new comment."""
    db = helpers_db.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=parent))

    body = flask.request.form.get('body', '').strip()
    if not body:
        flask.flash('Body cannot be empty.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=parent))
    
    comments_db.add_comment(db, parent, user, body)

    return flask.redirect(flask.url_for('posts.view_post', post_id=parent))

@blueprint.post('/comments/<int:comment_id>/delete/<int:parent>')
def delete_comment(comment_id, parent):
    """Delete a comment (only by its author)."""
    db = helpers_db.load_db()

    # must be logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to delete comments.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=parent))

    # must exist and belong to current user
    c = comments_db.get_comment_by_id(db, comment_id)
    if not c:
        flask.flash('Comment not found.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=parent))

    if c['user'] != user['username']:
        flask.flash('You can only delete your own comments.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=parent))

    # delete
    comments_db.delete_comment(db, comment_id)
    flask.flash('Comment deleted.', 'success')
    return flask.redirect(flask.url_for('posts.view_post', post_id=parent))
