import tinydb

def new_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return None
    user_record = {
            'username': username,
            'password': password,
            'crews': [],
            'friends': []
            }
    return users.insert(user_record)

def get_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.get((User.username == username) &
            (User.password == password))

def get_user_by_name(db, username):
    users = db.table('users')
    User = tinydb.Query()
    return users.get(User.username == username)

def delete_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.remove((User.username == username) &
            (User.password == password))



def add_user_crew(db, user, crew):
    users = db.table('users')
    User = tinydb.Query()
    if crew not in user['crews']:
        if users.get(User.username == crew):
            user['crews'].append(crew)
            users.upsert(user, (User.username == user['username']) &
                    (User.password == user['password']))
            return 'Membership to {} added successfully!'.format(crew), 'success'
        return 'User {} does not exist.'.format(crew), 'danger'
    return 'You are already a member of {}.'.format(crew), 'warning'

def remove_user_crew(db, user, crew):
    users = db.table('users')
    User = tinydb.Query()
    if crew in user['crews']:
        user['crews'].remove(crew)
        users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
        return 'Membership to {} successfully removed!'.format(crew), 'success'
    return 'You are not a member of {}.'.format(crew), 'warning'

def get_user_crews(db, user):
    users = db.table('users')
    User = tinydb.Query()
    crews = []
    for crew in user['crews']:
        crews.append(users.get(User.username == crew))
    return crews





def add_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend not in user['friends']:
        if users.get(User.username == friend):
            user['friends'].append(friend)
            users.upsert(user, (User.username == user['username']) &
                    (User.password == user['password']))
            return 'Friend {} added successfully!'.format(friend), 'success'
        return 'User {} does not exist.'.format(friend), 'danger'
    return 'You are already friends with {}.'.format(friend), 'warning'

def remove_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend in user['friends']:
        user['friends'].remove(friend)
        users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
        return 'Friend {} successfully unfriended!'.format(friend), 'success'
    return 'You are not friends with {}.'.format(friend), 'warning'

def get_user_friends(db, user):
    users = db.table('users')
    User = tinydb.Query()
    friends = []
    for friend in user['friends']:
        friends.append(users.get(User.username == friend))
    return friends
