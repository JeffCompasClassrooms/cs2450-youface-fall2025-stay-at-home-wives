import time
import tinydb

def get_crews_by_user(db, user):
    crews = db.table('posts')
    Crew = tinydb.Query()
    return crews.search(Crew.user==user['username'])

def get_crew_by_id(db, crew_id: int):
    table = db.table('crews')
    doc = table.get(doc_id=crew_id)
    if not doc:
        return None
    return doc

def add_crew(db, user, text, title=None):
    crews = db.table('crews')
    doc = {
        "user": user["username"],
        "title": title if title else None,
        "description": text,
        "time": time.time(),
        "members": 1,
    }
    return crews.insert(doc)

def edit_crew(db, crew_id, text, title=None):
    crews = db.table('crews')
    members = crews.get(doc_id=crew_id)['members']
    Crew = tinydb.Query()
    return crews.update({
        "title": title if title else None,
        "description": text,
        "time": time.time(),
        "members": members,}, 
        Crew.crew_id == crew_id)

def delete_crew(db, crew_id: int) -> bool:
    """Delete a crew by its TinyDB doc_id."""
    table = db.table('crews')
    return bool(table.remove(doc_ids=[crew_id]))
