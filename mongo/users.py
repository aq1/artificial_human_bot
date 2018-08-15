from pymongo.errors import DuplicateKeyError

from mongo.client import db


def get_user(chat_id):
    return db.users.find_one({
        'chat_id': chat_id,
    })


def save_user(user):
    try:
        db.users.save({
            'chat_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'last_project_time': '',
            'queries': [],
        })
    except DuplicateKeyError:
        pass


def add_query(chat_id, value):
    db.users.update({'chat_id': chat_id}, {'$addToSet': {'queries': value}})


def remove_query(chat_id, value):
    db.users.update({'chat_id': chat_id}, {'$pull': {'queries': value}})


def get_queries():
    result = set()
    for user in db.users.find({}):
        for q in user['queries']:
            result.add(q)
    return result
