from pymongo.errors import DuplicateKeyError

from mongo.client import db
from mongo import users


def get_last_project_time(query):
    return db.queries.find_one({'query': query})


def save_last_project_time(query, marketplace, time):
    db.queries.update(
        {'query': query},
        {'$set': {marketplace: time}},
        upsert=True,
    )


def get_projects(query, last_project_time, limit=10):
    if not last_project_time:
        last_project_time = ''

    return db.projects.find({
        'query': query,
        'time_updated': {'$gt': last_project_time},
    }).limit(limit)


def get_new_projects(chat_id, limit=10):
    projects = []
    user = users.get_user(chat_id)

    for market, last_seen_project in user['last_seen_project'].items():
        projects += db.projects.find({
            'market': market,
            'query': {'$in': user['queries']},
            'project_id': {'$gt': last_seen_project or 0},
        }).sort('project_id').limit(limit - len(projects))
        if len(projects) >= limit:
            break

    return projects[:limit]


def save_projects(projects):
    count = 0
    for project in projects:
        try:
            db.projects.save(project)
        except DuplicateKeyError:
            continue
        count += 1
    return count
