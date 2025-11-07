import time
import tinydb

def get_posts_by_user(db, user):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.user==user['username'])

def get_post_by_id(db, post_id: int):
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return None
    return ensure_shape(doc)

def increment_views(db, post_id: int):
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return
    p = ensure_shape(doc)
    p['views'] += 1
    table.update(p, doc_ids=[post_id])

def ensure_shape(p):
    if 'views' not in p:
        p['views'] = 0
    if 'image' not in p:
        p['image'] = None
    return p

def add_post(db, user, text, title=None, image_filename=None):
    posts = db.table('posts')
    doc = {
        # "parent": crew["crew_id"],
        "user": user["username"],
        "title": title if title else None,
        "text": text,
        "time": time.time(),
        "views": 0,
        "image": image_filename,
    }
    return posts.insert(doc)

def edit_post(db, post_id, text, title=None, image_filename=None):
    posts = db.table('posts')
    views = posts.get(doc_id=post_id)['views']
    Post = tinydb.Query()
    return posts.update({
        "title": title if title else None,
        "text": text,
        "time": time.time(),
        "views": views,
        "image": image_filename,}, 
        Post.post_id == post_id)

def delete_post(db, post_id: int) -> bool:
    """Delete a post by its TinyDB doc_id."""
    table = db.table('posts')
    return bool(table.remove(doc_ids=[post_id]))
