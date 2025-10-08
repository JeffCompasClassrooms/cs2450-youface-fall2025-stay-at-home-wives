import tinydb

statusMessages = {
        "invalidCredential": "invalidCredential",
        "usernameTaken": "usernameTaken",
        "success": "success"
        }

def checkUsername(username):
    if len(username) > 20:
        return False
    letterCount = 0
    for char in username:
        if (char.isalpha()):
            letterCount += 1
            break
    if letterCount < 1:
        return False
    return True

def checkPassword(password):
    if len(password) < 8:
        return False
    if len(password) > 20:
        return False
    letterCount = 0
    for char in username:
        if (char.isalpha()):
            letterCount += 1
            break
    if letterCount < 1:
        return False
    return True


def new_user(db, username, password):
    if (not checkUsername(username)):
        return statusMessages["invalidCredential"]
    if (not checkPassword(password)):
        return statusMessages["invalidCredential"]
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return statusMessages["usernameTaken"]
    user_record = {
            'username': username,
            'password': password,
            'friends': []
            }
    return statusMessages["success"]

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
