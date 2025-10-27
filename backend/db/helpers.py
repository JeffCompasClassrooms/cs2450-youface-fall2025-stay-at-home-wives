import tinydb

def load_db():
    return tinydb.TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))
