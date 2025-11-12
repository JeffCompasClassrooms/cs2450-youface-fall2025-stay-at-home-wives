import time
import tinydb
from db import posts as posts_db

# gets all crews associated with a given user
def get_crews_by_user(db, user):
    crews = db.table('posts')
    Crew = tinydb.Query()
    return crews.search(Crew.user==user['username'])

# gets a singular crew via its ID
def get_crew_by_id(db, crew_id: int):
    table = db.table('crews')
    doc = table.get(doc_id=crew_id)
    if not doc:
        return None
    return doc

# creates a new crew in the db
def add_crew(db, user, description, title=None):
    crews = db.table('crews')
    doc = {
        "user": user["username"],
        "title": title if title else None,
        "description": description,
        "time": time.time(),
        "members": 1,
    }
    return crews.insert(doc)

# edits the title and description of a crew in the db, updates time
def edit_crew(db, crew_id, text, title=None):
    crews = db.table('crews')
    Crew = tinydb.Query()
    return crews.update({
        "title": title if title else None,
        "description": text,
        "time": time.time(),}, 
        Crew.crew_id == crew_id)

# deletes a crew from the db and all its child posts
def delete_crew(db, crew_id: int) -> bool:
    """Delete a crew by its TinyDB doc_id."""
    table = db.table('crews')
    posts = db.table('posts')
    Post = tinydb.Query()
    child_posts = posts.search(Post.parent==crew_id)
    for post in child_posts:
        posts_db.delete_post(db, post.doc_id)
    return bool(table.remove(doc_ids=[crew_id]))
