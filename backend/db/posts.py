import time
import tinydb
from db import comments as comments_db

# gets all posts associated with a given user
def get_posts_by_user(db, user):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.user==user['username'])

#gets all comments associated with a post
def get_posts_by_crew(db, crew_id):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.parent==crew_id)

# gets a singular post via its ID
def get_post_by_id(db, post_id: int):
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return None
    return ensure_shape(doc)

# increments the views on a post
def increment_views(db, post_id: int):
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return
    p = ensure_shape(doc)
    p['views'] += 1
    table.update(p, doc_ids=[post_id])

# ensures all data is valid and follows conventions
def ensure_shape(p):
    if 'views' not in p:
        p['views'] = 0
    if 'image' not in p:
        p['image'] = None
    return p

# adds a new post to the db
def add_post(db, crew_id, user, text, title=None, image_filename=None):
    posts = db.table('posts')
    doc = {
        "parent": crew_id,
        "user": user["username"],
        "title": title if title else None,
        "text": text,
        "time": time.time(),
        "views": 0,
        "image": image_filename,
    }
    return posts.insert(doc)

# edits the title, text, and image of a post in db, updates the time
def edit_post(db, post_id, text, title=None, image_filename=None):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.update({
        "title": title if title else None,
        "text": text,
        "time": time.time(),
        "image": image_filename,}, 
        Post.post_id == post_id)

# deletes a post in db and all its child comments
def delete_post(db, post_id: int) -> bool:
    """Delete a post by its TinyDB doc_id."""
    table = db.table('posts')
    comments = db.table('comments')
    Comment = tinydb.Query()
    child_comments = comments.search(Comment.parent==post_id)
    for comment in child_comments:
        comments_db.delete_comment(db, comment.doc_id)
    return bool(table.remove(doc_ids=[post_id]))
