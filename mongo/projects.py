from pymongo.errors import DuplicateKeyError

from mongo.client import db


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


def save_projects(projects):
    count = 0
    for project in projects:
        try:
            db.projects.save(project)
        except DuplicateKeyError:
            continue
        count += 1
    return count
