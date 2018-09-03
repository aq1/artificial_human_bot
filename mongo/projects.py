import pymongo

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


def get_new_projects(chat_id, limit=20):
    projects = []
    user = users.get_user(chat_id)

    for market, last_seen_project in user['last_seen_project'].items():
        query = {
            'market': market,
            'query': {'$in': user['queries']},
            'project_id': {'$gt': last_seen_project or 0}
        }

        projects += db.projects.find(query).sort('project_id', pymongo.DESCENDING).limit(limit - len(projects))
        if len(projects) >= limit:
            break

    return projects[:limit]


def save_projects(projects):
    inserted, updated = 0, 0
    for project in projects:
        result = db.projects.update(
            {'market': project['market'], 'project_id': project['project_id']},
            project,
            upsert=True
        )
        inserted += int(not result['updatedExisting'])
        updated += int(result['updatedExisting'])

    return inserted, updated
