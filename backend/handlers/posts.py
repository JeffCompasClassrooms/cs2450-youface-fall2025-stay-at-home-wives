import flask
from db import posts as posts_db, helpers as helpers_db, users as users_db, comments as comments_db
#os for file paths, 
#uuid creates uniqe names for the files
#secure_filename removes dangerous chars from the file names
import os
import uuid
from werkzeug.utils import secure_filename

blueprint = flask.Blueprint("posts", __name__)

upload_folder = 'backend/uploads'
allowed_extensions={'jpg','png','jpeg','webp'}
max_file_size=8*1024*1024


@blueprint.route('/post/<int:crew_id>', methods=['POST'])
def post(crew_id):
    """Creates a new post."""
    db = helpers_db.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('crews.view_crew', crew_id=crew_id))

    title = flask.request.form.get('title', '').strip()
    text = flask.request.form.get('post', '').strip()
    if not text:
        flask.flash('Post cannot be empty.', 'danger')
        return flask.redirect(flask.url_for('crews.view_crew', crew_id=crew_id))

    image_filename=None
    if 'image' in flask.request.files:
        file=flask.request.files['image']
    if file and file.filename != '' and allowed_file_type(file.filename):
        originalFilename=secure_filename(file.filename)
        uniqueFilename = f"{uuid.uuid4().hex}_{originalFilename}"
        os.makedirs(upload_folder, exist_ok=True)
        file_path=os.path.join(upload_folder,uniqueFilename)
        file.save(file_path)
        if os.path.exists(file_path):
            image_filename=uniqueFilename
    else:
        if file and file.filename != '':
            flask.flash("Invalid IMG file")
    post_id=posts_db.add_post(db,crew_id,user,text,title,image_filename)

    return flask.redirect(flask.url_for('posts.view_post',post_id=post_id))

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
    
    # includes comments to be displayed on page
    comments = comments_db.get_comments_by_post(db, post_id)

    posts_db.increment_views(db, post_id)
    return flask.render_template('posts.html', post=p, username=username, user=user, comments=comments)


@blueprint.get('/posts/<int:parent>/new')
def new_post_form(parent):
    """serves page to make new post"""
    db = helpers_db.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('Please log in to create a post.', 'warning')
        return flask.redirect(flask.url_for('crews.view_crew', crew_id=parent))
    return flask.render_template('new_post.html', logged_in=True, user=user, username=username, parent=parent)

@blueprint.post('/posts/<int:post_id>/delete/<int:parent>')
def delete_post(post_id, parent):
    """Delete a post (only by its author)."""
    db = helpers_db.load_db()

    # must be logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to delete posts.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))

    # must exist and belong to current user
    p = posts_db.get_post_by_id(db, post_id)
    if not p:
        flask.flash('Post not found.', 'danger')
        return flask.redirect(flask.url_for('crews.view_crew', crew_id=parent))

    if p['user'] != user['username']:
        flask.flash('You can only delete your own posts.', 'danger')
        return flask.redirect(flask.url_for('posts.view_post', post_id=post_id))

    # delete
    posts_db.delete_post(db, post_id)
    flask.flash('Post deleted.', 'success')
    return flask.redirect(flask.url_for('crews.view_crew', crew_id=parent))
