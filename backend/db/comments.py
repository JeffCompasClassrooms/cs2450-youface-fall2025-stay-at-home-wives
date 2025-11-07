import time
import tinydb

def get_comments_by_user(db, user):
    comments = db.table('comments')
    Comment = tinydb.Query()
    return comments.search(Comment.user==user['username'])

def get_comment_by_id(db, comment_id: int):
    table = db.table('comments')
    doc = table.get(doc_id=comment_id)
    if not doc:
        return None
    return doc

def get_comment_by_post(db, post):
    comments = db.table('comments')
    Comment = tinydb.Query()
    return comments.search(Comment.parent_id==post['post_id'])

def add_comment(db, post, user, text):
    comments = db.table('comments')
    doc = {
        "parent": post["post_id"],
        "user": user["username"],
        "text": text,
        "time": time.time(),
    }
    return comments.insert(doc)

def edit_comment(db, comment_id, text):
    comments = db.table('comments')
    Comment = tinydb.Query()
    return comments.update({
        "text": text,
        "time": time.time(),}, 
        Comment.comment_id == comment_id)

def delete_comment(db, comment_id: int) -> bool:
    """Delete a crew by its TinyDB doc_id."""
    table = db.table('comments')
    return bool(table.remove(doc_ids=[comment_id]))