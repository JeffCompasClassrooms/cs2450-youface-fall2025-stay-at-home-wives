import time
import tinydb

def add_post(db, user, text, title=None, image_filename=None):
    posts = db.table('posts')
    doc = {
        "user": user["username"],
        "title": title if title else None,
        "text": text,
        "time": time.time(),
        "comments": [],
        "views": 0,
        "image": image_filename,
    }
    return posts.insert(doc)


def get_posts(db, user):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.user==user['username'])

def ensure_shape(p):
    if 'comments' not in p:
        p['comments'] = []
    if 'views' not in p:
        p['views'] = 0
    if 'image' not in p:
        p['image'] = None
    return p

def get_post_by_id(db, post_id: int):
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return None
    return ensure_shape(doc)

def add_comment(db, post_id: int, author_name: str, body: str):
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return False
    p = ensure_shape(doc)
    p['comments'].append({
        'author': author_name,
        'body': body,
        'time': time.time(),
    })
    table.update(p, doc_ids=[post_id])
    return True

def increment_views(db, post_id: int):
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return
    p = ensure_shape(doc)
    p['views'] += 1
    table.update(p, doc_ids=[post_id])

def delete_post(db, post_id: int) -> bool:
    """Delete a post by its TinyDB doc_id."""
    table = db.table('posts')
    return bool(table.remove(doc_ids=[post_id]))

def delete_comment(db, post_id: int, idx: int) -> bool:
    """Delete a single comment by index from a post."""
    table = db.table('posts')
    doc = table.get(doc_id=post_id)
    if not doc:
        return False
    p = ensure_shape(doc)
    if 0 <= idx < len(p['comments']):
        del p['comments'][idx]
        table.update(p, doc_ids=[post_id])
        return True
    return False
