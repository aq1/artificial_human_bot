import pymongo
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient

import settings

client = MongoClient(
    '{}:{}'.format(settings.MONGO_HOST, settings.MONGO_PORT),
    username=settings.MONGO_USER,
    password=settings.MONGO_PASSWORD,
    authSource=settings.MONGO_DB,
    authMechanism='SCRAM-SHA-1',
)

db = client[settings.MONGO_DB]
db.users.create_index('chat_id', unique=True)
db.projects.create_index((
    ('project_id', pymongo.DESCENDING),
    ('market', pymongo.DESCENDING)),
    unique=True,
)


def get_last_project_time(query):
    return db.queries.find_one({'query': query})


def save_last_project_time(query, marketplace, time):
    db.queries.update(
        {'query': query},
        {'$set': {marketplace: time}},
        upsert=True,
    )


def get_projects(query, last_project_time, skip=0):
    if not last_project_time:
        last_project_time = ''

    return db.projects.find({
        'query': query,
        'time_updated': {'$gt': last_project_time},
    })


def save_projects(projects):
    count = 0
    for project in projects:
        try:
            db.projects.save(project)
        except DuplicateKeyError:
            continue
        count += 1
    return count


def get_user(chat_id):
    return db.user.find_one({
        'chat_id': chat_id,
    })


def save_user(user):
    try:
        db.user.save({
            'chat_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'last_project_time': '',
            'stop_words': [],
        })
    except DuplicateKeyError:
        pass
