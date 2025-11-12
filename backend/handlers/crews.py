import flask
from db import crews as crews_db, helpers as helpers_db, users as users_db, posts as posts_db
blueprint = flask.Blueprint("crews", __name__)


@blueprint.route('/crew', methods=['POST'])
def post():
    """Creates a new crew."""
    db = helpers_db.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    title = flask.request.form.get('title', '').strip()
    description = flask.request.form.get('description', '').strip()
    if not title:
        flask.flash('Title cannot be empty.', 'danger')
        return flask.redirect(flask.url_for('login.index'))
    
    crew_id=crews_db.add_crew(db, user, description, title)

    return flask.redirect(flask.url_for('crews.view_crew',crew_id=crew_id))

@blueprint.get('/crews/<int:crew_id>')
def view_crew(crew_id):
    """Show a single crew with posts."""
    db = helpers_db.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password) if username and password else None

    c = crews_db.get_crew_by_id(db, crew_id)
    if not c:
        return ("Crew not found", 404)
    
    # includes posts to be displayed on page
    posts = posts_db.get_posts_by_crew(db, crew_id)

    return flask.render_template('crews.html', crew=c, username=username, user=user, posts=posts)

@blueprint.get('/crews/new')
def new_crew_form():
    """Serves form to make a new crew"""
    db = helpers_db.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('Please log in to create a crew.', 'warning')
        return flask.redirect(flask.url_for('login.index'))
    return flask.render_template('new_crew.html', logged_in=True, user=user, username=username)

@blueprint.post('/crews/<int:crew_id>/delete')
def delete_crew(crew_id):
    """Delete a crew (only by its author)."""
    db = helpers_db.load_db()

    # must be logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users_db.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to delete crews.', 'danger')
        return flask.redirect(flask.url_for('crews.view_crew', crew_id=crew_id))

    # must exist and belong to current user
    c = crews_db.get_crew_by_id(db, crew_id)
    if not c:
        flask.flash('crew not found.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    if c['user'] != user['username']:
        flask.flash('You can only delete your own crews.', 'danger')
        return flask.redirect(flask.url_for('crews.view_crew', crew_id=crew_id))

    # delete
    crews_db.delete_crew(db, crew_id)
    flask.flash('Crew deleted.', 'success')
    return flask.redirect(flask.url_for('login.index'))
