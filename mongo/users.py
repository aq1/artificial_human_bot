from pymongo.errors import DuplicateKeyError

from mongo.client import db


def get_all_user():
    return db.users.find({})


def get_user(chat_id):
    return db.users.find_one({
        'chat_id': chat_id,
    })


def update_last_seen_projects(chat_id, last_seen_projects):
    db.users.update(
        {'chat_id': chat_id},
        {
            '$set': {
                'last_seen_project.{}'.format(k): v for (k, v) in last_seen_projects.items()
            }
        },
    )


def save_user(user):
    try:
        db.users.save({
            'chat_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'queries': [],
            'last_seen_project': {
                'freelancer': None,
                'upwork': None,
                'guru': None,
                'people_per_hour': None,
            }
        })
    except DuplicateKeyError:
        pass


def add_query(chat_id, value):
    db.users.update({'chat_id': chat_id}, {'$addToSet': {'queries': value}})


def remove_query(chat_id, value):
    db.users.update({'chat_id': chat_id}, {'$pull': {'queries': value}})


def get_queries(chat_id=None):
    result = set()
    find_query = {'chat_id': chat_id} if chat_id else {}
    for user in db.users.find(find_query):
        for q in user['queries']:
            result.add(q)
    return result
