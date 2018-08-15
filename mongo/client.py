import pymongo
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
