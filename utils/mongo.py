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


def get_last_project_time(query):
    return db.queries.find_one({'query': query})


def save_last_project_time(query, marketplace, time):
    db.queries.update(
        {'query': query},
        {'$set': {marketplace: time}},
        upsert=True,
    )


def save_projects(projects):
    db.projects.insert_many(projects)
