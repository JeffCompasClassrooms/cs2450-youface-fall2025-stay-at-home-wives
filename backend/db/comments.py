import time
import tinydb

# gets all comments associated with a user
def get_comments_by_user(db, user):
    comments = db.table('comments')
    Comment = tinydb.Query()
    return comments.search(Comment.user==user['username'])

# gets a singular comment via its ID
def get_comment_by_id(db, comment_id: int):
    table = db.table('comments')
    doc = table.get(doc_id=comment_id)
    if not doc:
        return None
    return doc

#gets all comments associated with a post
def get_comment_by_post(db, post_id):
    comments = db.table('comments')
    Comment = tinydb.Query()
    return comments.search(Comment.parent_id==post_id)

# adds a new comment to the db
def add_comment(db, post_id, user, body):
    comments = db.table('comments')
    doc = {
        "parent": post_id,
        "user": user["username"],
        "body": body,
        "time": time.time(),
    }
    return comments.insert(doc)

# edits the text of a comment in db, updates time
def edit_comment(db, comment_id, text):
    comments = db.table('comments')
    Comment = tinydb.Query()
    return comments.update({
        "text": text,
        "time": time.time(),}, 
        Comment.comment_id == comment_id)

# deletes a comment from db
def delete_comment(db, comment_id: int) -> bool:
    """Delete a crew by its TinyDB doc_id."""
    table = db.table('comments')
    return bool(table.remove(doc_ids=[comment_id]))